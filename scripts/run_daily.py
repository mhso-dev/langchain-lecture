"""Replay the released daily starter notebooks, including the six-day Codex workbook."""
import ast
import asyncio
from contextlib import chdir, redirect_stdout
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
from zipfile import ZipFile

DAILY = Path(__file__).resolve().parents[1]/"dist"/"daily"
DAYS = [*range(2,43),*range(53,86),*range(117,121)]

def replay(file):
    scope = {"__name__":"__main__"}
    cells = json.loads(file.read_bytes())["cells"]
    async def execute():
        for cell in cells:
            if cell["cell_type"] != "code":
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
            records = replay(DAILY/name)
            (out/(Path(name).stem+".json")).write_text(json.dumps(records,ensure_ascii=False,indent=2))
            print(name,len(records),"OK",flush=True)

if __name__ == "__main__":
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True,exist_ok=True)
    if len(sys.argv)>2:
        run_set(sys.argv[2:],out)
    else:
        assert len(list(DAILY.glob("day*.ipynb"))) == len(DAYS) == 78
        with ZipFile(DAILY/"all-labs.zip") as z:
            for d in DAYS:
                name = f"day{d:03}.ipynb"
                assert z.read(name) == (DAILY/name).read_bytes(), name
        sets = [[f"day{d:03}.ipynb"] for d in DAYS if not 80<=d<=85]
        sets.append([f"day{d:03}.ipynb" for d in range(80,86)])
        sets.append(["codex-harness.ipynb"])
        bad=[]
        for group in sets:
            if subprocess.run([sys.executable,__file__,str(out),*group]).returncode:
                bad.append(group)
        if bad:
            raise SystemExit(str(bad))
