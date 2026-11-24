"""Run the student and solved notebooks, verify outputs, and check the 21→22 handoff.

Run python scripts/check_chapter22.py; add --require-chroma for the release gate.
The verifier needs the Chapter 21 verifier's packages and faiss-cpu. Install
chromadb to check the database in a fresh interpreter. All writes are temporary.
"""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from contextlib import chdir
from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat

from check_chapter20 import run_cells, stdout

SITE = Path(__file__).resolve().parents[1] / "site"
CHAPTER = SITE / "chapter22"


def load_notebook(day):
    path = SITE / f"chapter{day}" / f"chapter{day}.ipynb"
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    return notebook


def folded_answers(notebook):
    """Read the solution and output from the notes immediately below each task."""
    answers = {}
    for cell, notes in zip(notebook.cells, notebook.cells[1:]):
        if cell.cell_type != "code" or "<details" not in notes.source:
            continue
        code, result = re.findall(r"<pre><code>(.*?)</code></pre>", notes.source, re.S)
        answers[cell.id] = html.unescape(code), html.unescape(result)
    return answers


def published_cells(notebook):
    body = (CHAPTER / "index.html").read_text(encoding="utf-8")
    articles = re.findall(
        r'<article class="notebook-cell" data-cell="(\d+)" data-task="([01])">(.*?)</article>',
        body, re.S,
    )
    cells = {c.id: c for c in notebook.cells if c.cell_type == "code"}
    answers = folded_answers(notebook)
    seen = set()
    for number, task, article in articles:
        key = f"code-{number}"
        assert key not in seen, key
        seen.add(key)
        blocks = [html.unescape(re.sub(r"<[^>]+>", "", block)) for block in
                  re.findall(r"<pre[^>]*><code[^>]*>(.*?)</code></pre>", article, re.S)]
        output = re.search(r'<div class="output">.*?<pre[^>]*>(.*?)</pre>', article, re.S)
        assert blocks[0] == cells[key].source, (key, "web/notebook code")
        if task == "1":
            answer, result = answers[key]
            assert blocks == [cells[key].source, answer], (key, "folded answer")
            assert re.search(r'<details\b(?![^>]*\bopen\b)[^>]*>', article)
            assert not stdout(cells[key]), (key, "unexpected starter output")
        else:
            assert key not in answers, key
            result = stdout(cells[key])
        assert output and html.unescape(output[1]) == result, (key, "web/notebook output")
    assert seen == cells.keys() and answers, "missing article, task or code cell"
    return cells, answers


def prepare_handoff(directory):
    """Generate the real preceding lesson's solution in the student's workspace."""
    chapter = SITE / "chapter21"
    for name in ("guide-records.json", "branch-guide.txt"):
        shutil.copy(chapter / name, directory / name)
    upstream = load_notebook(21)
    answers = folded_answers(upstream)
    assert answers
    for c in upstream.cells:
        if c.id in answers:
            c.source = answers[c.id][0]
    with chdir(directory):
        run_cells(upstream, directory)
    saved = json.loads((directory / "chapter21-output/desk-hours.json").read_text(encoding="utf-8"))
    pages = (directory / "branch-guide.txt").read_text(encoding="utf-8").split("\f")
    assert saved["id"] == "branch-2:225" and saved["page"] == 2
    assert saved["text"] == pages[1][saved["start"]:saved["end"]]
    return saved


def check_database(path):
    """Called after the authoring kernel has stopped; no ingest can occur here."""
    import chromadb
    client = chromadb.PersistentClient(path=str(path))
    pages = (CHAPTER / "branch-guide.txt").read_text(encoding="utf-8").split("\f")
    for item in client.list_collections():
        name = item if isinstance(item, str) else item.name
        collection = client.get_collection(name, embedding_function=None)
        ids = set(collection.get()["ids"])
        if not {"branch-2:133", "branch-2:225"}.issubset(ids):
            continue
        for vector, chunk_id in [([1, 1, 0], "branch-2:225"), ([1, 0, 1], "branch-2:133")]:
            hit = collection.query(query_embeddings=[vector], n_results=1,
                                   include=["documents", "distances", "metadatas"])
            assert hit["ids"] == [[chunk_id]]
            assert hit["distances"] == [[0.0]]
            metadata = hit["metadatas"][0][0]
            assert metadata["page"] == 2 and metadata["source"] == "branch-guide.txt"
            assert hit["documents"][0][0] == pages[1][metadata["start"]:metadata["end"]]
        print("Chroma fresh interpreter: two queries returned the stored IDs, pages and zero distances.")
        return
    raise AssertionError("Reopened database does not contain the chapter 21 chunks.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-chroma", action="store_true")
    parser.add_argument("--database", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--run-mode", choices=("starter", "solutions"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.database:
        check_database(args.database)
        return
    if args.run_mode:
        check_execution(args.run_mode)
        return
    if find_spec("faiss") is None:
        parser.exit(2, "Install faiss-cpu in the verifier's Python environment.\n")
    for mode in ("starter", "solutions"):
        environment = dict(os.environ, ANONYMIZED_TELEMETRY="False")
        subprocess.run([sys.executable, __file__, "--run-mode", mode], check=True, env=environment)
    if find_spec("chromadb") is None:
        message = "Chroma unavailable: database writes and fresh-process reads were not executed."
        if args.require_chroma:
            parser.exit(2, message + "\n")
        print(message)


def expected_live_output(sample, time_record):
    """The download stores the observations from the authoring kernel without Chroma."""
    if sample.startswith("chromadb 미설치 · 저장"):
        return "branch-2:133"
    if sample.startswith("chromadb 미설치 · 시간표 등록"):
        return "2 건 저장"
    if sample.startswith("chromadb 미설치 · 검색 결과"):
        return "branch-2:225 branch-guide.txt 2\n" + time_record["text"]
    return sample.replace("Chroma 비교 미실행", "같은 1위 True")


def check_execution(mode):
    notebook = load_notebook(22)
    cells, answers = published_cells(notebook)
    expected = {key: stdout(c) for key, c in cells.items()}
    if mode == "solutions":
        for key, (code, result) in answers.items():
            cells[key].source = code
            expected[key] = result
    with TemporaryDirectory() as folder:
        directory = Path(folder)
        record = json.loads((CHAPTER / "desk-hours.json").read_text(encoding="utf-8"))
        for name in ("guide-records.json", "branch-guide.txt"):
            assert (SITE / "chapter21" / name).read_bytes() == (CHAPTER / name).read_bytes()
        if mode == "solutions":
            assert prepare_handoff(directory) == record
            # If the exported 21 file is ignored or has lower priority than the
            # reference copy, the notebook must fail against this invalid decoy.
            decoy = {**record, "id": "wrong-file"}
            (directory / "desk-hours.json").write_text(json.dumps(decoy), encoding="utf-8")
        probe = nbformat.v4.new_code_cell(
            """assert desk["id"] == "branch-2:225" and desk["page"] == 2
assert original_text(desk, pages) == pages[2][225:279]
assert stored_vectors == [[1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
for question, wanted_id in [
        ("토요일 안내 데스크는 몇 시에 닫나요?", "branch-2:225"),
        ("안내 데스크에 습득한 물건을 맡기나요?", "branch-2:133")]:
    q = np.array([vector(question, branch_terms)], dtype="float32")
    dist, pos = index_lab.search(q, 2)
    assert dist.tolist() == [[0.0, 2.0]] and keys[int(pos[0, 0])] == wanted_id
for changed in ({"source": "wrong.txt"}, {"page": 1}, {"document_id": "branch-1"},
                {"id": "branch-2:224"}, {"start": -1}, {"end": 278},
                {"text": "다른 본문"}):
    try:
        original_text({**desk, **changed}, pages)
    except ValueError:
        pass
    else:
        raise AssertionError(changed)
parking = np.array([vector("주차 요금은?", branch_terms)], dtype="float32")
assert index_lab.search(parking, 2)[0].tolist() == [[2.0, 2.0]]
print(json.dumps([desk, pages[2], branch_terms, chunks], ensure_ascii=False))"""
        )
        notebook.cells.append(probe)
        with chdir(directory):
            run_cells(notebook, directory)
        desk, page, terms, chunks = json.loads(stdout(probe))
        assert desk == record
        body = (CHAPTER / "index.html").read_text(encoding="utf-8")
        raw = re.search(r'<script type="application/json">(.*?)</script>', body, re.S)
        assert raw, "missing interactive source text"
        visual = json.loads(raw[1])
        assert visual["vocabulary"] == terms and visual["page"] == page
        fields = ("id", "document_id", "text", "page", "source", "start", "end")
        assert [[v[k] for k in fields] for v in visual["chunks"]] == [
            [v[k] for k in fields] for v in chunks
        ]
        has_database = find_spec("chromadb") is not None
        for key, text in expected.items():
            if has_database:
                text = expected_live_output(text, record)
            assert stdout(cells[key]) == text, (mode, key, stdout(cells[key]), text)
        if has_database:
            paths = list(directory.rglob("chroma.sqlite3"))
            assert len(paths) == 1, "could not locate the persisted student database"
            subprocess.run([sys.executable, __file__, "--database", str(paths[0].parent)], check=True)
    print(f"{mode}: {len(cells)} cells, {len(answers)} folded exercises, FAISS searches and original spans checked.")


if __name__ == "__main__":
    main()
