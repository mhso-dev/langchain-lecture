"""Replay the first unit's examples and its folded answers in separate processes."""
import argparse
from contextlib import redirect_stdout
from html import unescape
from html.parser import HTMLParser
from io import StringIO
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1] / "site" / "pre-mid"


class CodeBlocks(HTMLParser):
    """Read the exact text a student copies out of each HTML pre element."""
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            assert self.current is None, "중첩된 pre 태그가 코드를 끊었습니다."
            self.current = []

    def handle_data(self, text):
        if self.current is not None:
            self.current.append(text)

    def handle_endtag(self, tag):
        if tag == "pre":
            self.blocks.append("".join(self.current).strip())
            self.current = None


def check_html(path):
    folder = ROOT.parents[1] / "dist" / "pre-mid" / path.parent.relative_to(ROOT)
    assert path.read_bytes() == (folder / path.name).read_bytes()
    if path.name != "lesson.ipynb":
        return
    page = CodeBlocks()
    page.feed((folder / "index.html").read_text(encoding="utf-8"))
    for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
        source = "".join(cell["source"])
        expected = []
        if cell["cell_type"] == "code":
            expected.append(source)
            expected.extend("".join(o["text"]) for o in cell["outputs"] if o.get("name") == "stdout")
        elif source.strip().startswith("<details>"):
            answer = CodeBlocks()
            answer.feed(source)
            expected.extend(answer.blocks)
        for block in expected:
            assert block.strip() in page.blocks, (path, cell["id"], "HTML 코드 또는 출력 불일치")


def replay(path, mode):
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    namespace = {"__name__": "__main__"}
    count = 0
    for index, cell in enumerate(cells):
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell["source"])
        expected = "".join("".join(o["text"]) for o in cell["outputs"] if o.get("name") == "stdout")
        if mode == "solution" and cell["metadata"].get("role") == "exercise":
            answer = cells[index + 1]
            assert answer["metadata"].get("role") == "solution", (path, cell["id"])
            blocks = re.findall(r"<pre>(.*?)</pre>", "".join(answer["source"]), re.S)
            assert len(blocks) >= 2, (path, cell["id"])
            source, expected = [unescape(re.sub(r"</?code>", "", block)) for block in blocks[:2]]
        output = StringIO()
        with redirect_stdout(output):
            exec(compile(source, f"{path.name}:{cell['id']}", "exec"), namespace)
        if output.getvalue().rstrip() != expected.rstrip():
            raise AssertionError(f"{path}:{cell['id']} {mode}: {output.getvalue()!r} != {expected!r}")
        count += 1
    print(f"{path.relative_to(ROOT)} · {mode} · {count}셀 일치")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path)
    parser.add_argument("--mode", choices=("starter", "solution"))
    args = parser.parse_args()
    if args.path:
        replay(args.path, args.mode)
    else:
        for path in sorted(ROOT.rglob("*.ipynb")):
            check_html(path)
            for mode in ("starter", "solution"):
                subprocess.run([sys.executable, __file__, "--path", str(path), "--mode", mode], check=True)
