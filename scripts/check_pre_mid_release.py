"""Validate the notebooks students actually download, including the RAG-to-evaluation handoff."""
import argparse
import ast
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class SolutionCode(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "code" and self.current is None:
            self.current = []

    def handle_endtag(self, tag):
        if tag == "code" and self.current is not None:
            self.blocks.append("".join(self.current))
            self.current = None

    def handle_data(self, value):
        if self.current is not None:
            self.current.append(value)


def compile_cell(text, filename):
    if text.startswith("%%writefile "):
        text = text.partition("\n")[2]
    lines = [line for line in text.splitlines() if not line.lstrip().startswith(("%pip ", "!pip "))]
    compile("\n".join(lines), filename, "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)


def check_release():
    with ZipFile(DIST / "daily/pre-mid.zip") as z, ZipFile(DIST / "daily/all-labs.zip") as all_labs:
        for path in (DIST / "pre-mid").rglob("*"):
            if path.is_file() and path.suffix not in {".html", ".pyc"}:
                key = path.relative_to(DIST).as_posix()
                assert z.read(key) == all_labs.read(key) == path.read_bytes(), key
        for n in range(14, 43):
            slug = f"chapter{n:02}"
            name = slug + ".ipynb"
            daily = f"day{n:03}.ipynb"
            source = (ROOT / "site" / slug / name).read_bytes()
            assert source == z.read(name) == (DIST / slug / name).read_bytes(), name
            assert source == all_labs.read(daily) == (DIST / "daily" / daily).read_bytes(), name
            book = json.loads(source)
            assert re.match(fr"^#\s*{n}장", "".join(book["cells"][0]["source"])), name
            assert len({c["id"] for c in book["cells"]}) == len(book["cells"]), name
            assert any("<details" in "".join(c["source"]) for c in book["cells"]), name
            for c in book["cells"]:
                text = "".join(c["source"])
                if c["cell_type"] == "code":
                    compile_cell(text, name + ":" + c["id"])
                elif text.lstrip().startswith("<details"):
                    for code in re.findall(r"<pre[^>]*>\s*<code[^>]*>.*?</code>\s*</pre>", text, re.S):
                        parser = SolutionCode()
                        parser.feed(code)
                        for block in parser.blocks:
                            compile_cell(block, name + ":" + c["id"])
    print("14~42장 원본·배포·실습 노트북 및 묶음 자료 일치, 코드 셀과 예시 풀이 문법 확인")


def check_handoff():
    # Only the external model/search responses are controlled for this repeatable path test.
    with TemporaryDirectory() as tmp, ZipFile(DIST / "daily/pre-mid.zip") as z:
        z.extractall(tmp)
        docs = Path(tmp) / "pre-mid" / "documents"
        sys.path[:0] = [str(docs / s) for s in ("rag", "graph", "evaluation")]
        from rag_lab import read_pages
        from recorder_graph import ask, assemble_graph
        from eval_lab import assessment, examples, gold_page
        pages = [p for pdf in sorted((docs / "sources").glob("recorder-*.pdf")) for p in read_pages(pdf)]
        by_id = {p["id"]: p for p in pages}
        sets = [examples("dev"), examples("holdout")]
        assert not {r["inputs"]["id"] for r in sets[0]} & {r["inputs"]["id"] for r in sets[1]}
        for rows in sets:
            for row in rows:
                gold = gold_page(row["outputs"])
                if gold:
                    page = by_id[gold]
                    assert page["model"] == row["inputs"]["model"] and page["edition"] == row["inputs"]["edition"], row
                    scores = assessment({"action":"answer", "citations":[gold], "candidates":[gold]}, row["outputs"])
                    assert all(r["score"] == 1 for r in scores["results"])
        target = next(p for p in pages if p["model"] == "A" and p["edition"] == "1.1")
        other = next(p for p in pages if p["model"] == "B")
        for results, expected in [([[target]], ["retrieve","judge","compose"]),
                                  ([[other],[target]], ["retrieve","judge","rewrite","retrieve","judge","compose"]),
                                  ([[other],[other]], ["retrieve","judge","rewrite","retrieve","judge","hold"])]:
            batches = iter(results)
            graph = assemble_graph(lambda q: next(batches), lambda q, ps: ([dict(ps[0], quote=ps[0]["text"][:14])], "인용 확인"),
                                   lambda q, ps: ps[0]["quote"], lambda q, m, e: q+" "+m+" "+e)
            state = ask(graph, "녹음 중 표시등을 끌 수 있나요?", "A", "1.1")
            assert state["path"] == expected, state["path"]
    print("ZIP에서 PDF 읽기, 개발·확인 질문의 쪽수·판본, 그래프 세 경로와 검색 평가 인계 확인")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", action="store_true")
    args = parser.parse_args()
    check_release()
    if args.handoff:
        check_handoff()
