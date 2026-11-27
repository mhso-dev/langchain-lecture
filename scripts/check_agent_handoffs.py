"""Check the published SQL-to-agent course using fresh IPython kernels.

Run with Python 3.12 and the course dependencies (including ipykernel).
Only the cumulative practice is executed. No model API key is used.
"""
import argparse
import asyncio
from contextlib import redirect_stdout
from html import unescape
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

SITE = Path(__file__).resolve().parents[1] / "dist"


async def run_cells(book, chapter, solution):
    from ipykernel.inprocess.manager import InProcessKernelManager

    manager = InProcessKernelManager()
    manager.start_kernel()
    try:
        shell = manager.kernel.shell
        for index, cell in enumerate(book["cells"]):
            if cell["cell_type"] != "code" or not cell["id"].startswith("desk-"):
                continue
            source = "".join(cell["source"])
            if solution and index + 1 < len(book["cells"]):
                answer = "".join(book["cells"][index + 1]["source"])
                match = re.match(r"<details.*?<pre><code>(.*?)</code></pre>", answer, re.S)
                if match:
                    source = unescape(match[1])
            if chapter == 54 and solution and cell["id"] == "desk-example":
                assert source.count("revised_days = 14") == 1
                source = source.replace("revised_days = 14", "revised_days = 21")
            buf = io.StringIO()
            with redirect_stdout(buf):
                run = await shell.run_cell_async(
                    source,
                    transformed_cell=shell.transform_cell(source),
                    store_history=False,
                    silent=True,
                )
            error = run.error_before_exec or run.error_in_exec
            if error:
                raise RuntimeError(f"{chapter}장 {cell['id']} 실행 오류") from error
            if cell["id"] == "desk-read" and chapter > 53:
                assert "내 파일" in buf.getvalue(), (chapter, "이전 산출물 미사용")
    finally:
        manager.shutdown_kernel()


def check_series(solution):
    with TemporaryDirectory() as temp:
        work = Path(temp)
        for day in range(53, 68):
            folder = work / f"chapter{day:02}"
            folder.mkdir()
            args = [sys.executable, str(Path(__file__).resolve()), "--chapter", str(day)]
            if solution:
                args.append("--solution")
            subprocess.run(args, cwd=folder, check=True)
        handoff = json.loads((work / "my-course/agent-api-case.json").read_text())
        duration = "21일" if solution else "14일"
        assert handoff["request"] == {"question": "대출 기간은 며칠인가요?", "k": 2}
        assert handoff["expected"]["answer_contains"] == duration
        assert handoff["expected"]["source_id"] == handoff["service_record"]["id"] == "loan-01"
        assert duration in handoff["service_record"]["text"]
        print(f"53~67장 {'풀이' if solution else '시작본'} 연속 실행 · {duration} · loan-01")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", type=int, choices=range(53, 68), help=argparse.SUPPRESS)
    parser.add_argument("--solution", action="store_true", help=argparse.SUPPRESS)
    options = parser.parse_args()
    if options.chapter:
        name = f"chapter{options.chapter:02}"
        payload = json.loads((SITE / name / f"{name}.ipynb").read_text())
        asyncio.run(run_cells(payload, options.chapter, options.solution))
    else:
        for key in ("OPENAI_API_KEY", "LANGSMITH_API_KEY", "LANGCHAIN_API_KEY"):
            os.environ.pop(key, None)
        check_series(False)
        check_series(True)
