"""Run the student cells and then the answer replacements in fresh namespaces."""
from contextlib import redirect_stdout
from html import unescape
from io import StringIO
import os
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ANSWER = re.compile(r"<pre><code>(.*?)</code></pre><pre>(.*?)</pre>", re.S)


def replay(notebook, use_answers):
    cells = json.loads(notebook.read_text())["cells"]
    kernel = {"__name__": "__main__"}
    programs = answers = 0
    for i, cell in enumerate(cells):
        if cell["cell_type"] != "code":
            continue
        if "live-model" in cell.get("metadata", {}).get("tags", []):
            program = compile("".join(cell["source"]), notebook.name, "exec")
            if os.environ.get("OPENAI_API_KEY"):
                exec(program, kernel)
            else:
                print(f"{notebook.name}: API 키 없음 · 실제 모델 셀 미실행")
            continue
        programs += 1
        code = "".join(cell["source"])
        expected = "".join("".join(o["text"]) for o in cell["outputs"])
        following = "".join(cells[i + 1]["source"]) if i + 1 < len(cells) else ""
        if following.startswith('<details class="notebook-answer">'):
            answers += 1
            if use_answers:
                match = ANSWER.search(following)
                assert match, (notebook.name, cell["id"])
                code, expected = map(unescape, match.groups())
        output = StringIO()
        location = f"{notebook.name}#{cell['id']}"
        with redirect_stdout(output):
            exec(compile(code, location, "exec"), kernel)
        assert output.getvalue() == expected, (location, expected, output.getvalue())
    return programs, answers


if __name__ == "__main__":
    paths = sorted((ROOT / "coursebook").glob("*.ipynb"))
    cells = tasks = 0
    for path in paths:
        replay(path, False)
        n, a = replay(path, True)
        cells += n
        tasks += a
    print(f"통합 노트북 {len(paths)}개 · 코드 셀 {cells}개 · 풀이 교체 {tasks}개 출력 일치")
