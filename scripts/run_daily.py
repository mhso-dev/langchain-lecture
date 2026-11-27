"""Replay the released daily starter notebooks, including the six-day Codex workbook."""
import ast
import asyncio
from contextlib import chdir, redirect_stdout
import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
from zipfile import ZipFile

DAILY = Path(__file__).resolve().parents[1]/"dist"/"daily"
DAYS = [*range(1,43),*range(53,86),*range(117,121)]

def replay(file):
    scope = {"__name__":"__main__"}
    cells = json.loads(file.read_bytes())["cells"]
    async def execute():
        for cell in cells:
            if cell["cell_type"] != "code":
                continue
            if (os.environ.get("HK_COURSE_OFFLINE") == "1"
                    and file.name in {"day055.ipynb", "day064.ipynb", "day066.ipynb", "day067.ipynb"}
                    and cell["id"] == "solo-walkthrough-code"):
                yield {"id": cell["id"], "status": "skipped", "reason": "외부 모델을 호출하는 개인 실습"}
                continue
            src = "".join(cell["source"])
            label = f"{file.name}:{cell['id']}"
            with redirect_stdout(io.StringIO()) as captured:
                code = compile(src,label,"exec",flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
                result = eval(code,scope)
                if result is not None:
                    await result
            yield {"id":cell["id"],"stdout":captured.getvalue().strip()}
    async def collect():
        return [item async for item in execute()]
    return asyncio.run(collect())

def run_set(names,out):
    with TemporaryDirectory() as work, chdir(work):
        Path("daily_resources").symlink_to(DAILY/"daily_resources",target_is_directory=True)
        for name in names:
            if name.startswith("day") and 14 <= int(name[3:6]) <= 42:
                # These downloads are aliases of the same 29 canonical notebooks.
                # check_pre_mid_release checks the alias bytes, code and offline graph paths.
                continue
            book = json.loads((DAILY/name).read_bytes())
            if book.get("metadata", {}).get("execution") == "live-workshop":
                # The pre-mid checker validates the canonical workbook without spending API credits.
                print(name, "라이브 수업 · 자동 실행 제외", flush=True)
                continue
            records = replay(DAILY/name)
            (out/(Path(name).stem+".json")).write_text(json.dumps(records,ensure_ascii=False,indent=2))
            skipped = sum(row.get("status") == "skipped" for row in records)
            print(name, len(records) - skipped, "실행,", skipped, "미실행", flush=True)

if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True,exist_ok=True)
    if len(sys.argv)>2:
        run_set(sys.argv[2:],out)
    else:
        assert len(list(DAILY.glob("day*.ipynb"))) == len(DAYS) == 79
        with ZipFile(DAILY/"all-labs.zip") as z:
            for d in DAYS:
                name = f"day{d:03}.ipynb"
                assert z.read(name) == (DAILY/name).read_bytes(), name
        sets = [[f"day{d:03}.ipynb"] for d in DAYS if not 68<=d<=85]
        sets.append([f"day{d:03}.ipynb" for d in range(68,86)])
        sets.append(["codex-harness.ipynb"])
        bad=[]
        for group in sets:
            if subprocess.run([sys.executable,__file__,str(out),*group]).returncode:
                bad.append(group)
        if bad:
            raise SystemExit(str(bad))
