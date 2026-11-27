"""Execute published cells in a fresh directory and record actual per-cell output."""
import argparse
import ast
import asyncio
from contextlib import chdir, redirect_stdout
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PENDING = [14,15,16,20,22,23,24,25,30,31,32,35,36,37,38,39,40,41,42,45,46,47,48,53,54,60,61,62,71,72,76,77]

def run(day, solved, full):
    chapter = ROOT/'dist'/f'chapter{day:02}'
    file = chapter/(chapter.name+'.ipynb')
    cells = json.loads(file.read_bytes())['cells']
    record = {'chapter':day, 'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
              'mode':'solution' if solved else 'student', 'cells':[]}
    with tempfile.TemporaryDirectory() as work, chdir(work):
        for item in chapter.iterdir():
            if item.suffix in ('.pdf','.txt','.json','.csv'):
                shutil.copy2(item,item.name)
        Path('daily_resources').symlink_to(ROOT/'dist/daily/daily_resources',target_is_directory=True)
        Path('pre-mid').symlink_to(ROOT/'dist/pre-mid', target_is_directory=True)
        scope={'__name__':'__main__'}
        for idx,cell in enumerate(cells):
            if cell['cell_type']!='code':
                continue
            key=cell['id']
            code=''.join(cell['source'])
            if solved and idx+1<len(cells):
                following=''.join(cells[idx+1]['source']).lstrip()
                if following.startswith('<details'):
                    match=re.search(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',following,re.S)
                    if match:
                        answer = html.unescape(match[1])
                        # The RAG exercise answers finish the provided starter inputs.
                        code = code + "\n" + answer if key.startswith("carry-try-") else answer
            if full:
                if day==60:code=code.replace('run_profile_db = False','run_profile_db = True')
                if day==71:
                    code=code.replace('image_id = ""','image_id = "python:3.12-slim"')
                    if solved:code=code.replace('run_image = False','run_image = True')
                if day==72:code=code.replace('run_stack = False','run_stack = True')
                scope['os']=os
            captured=io.StringIO()
            result={'id':key}
            with redirect_stdout(captured):
                try:
                    product=eval(compile(code,file.name+':'+key,'exec',flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT),scope)
                    if product is not None:asyncio.run(product)
                except Exception:
                    result['error']=traceback.format_exc()
            result['stdout']=captured.getvalue().strip()
            record['cells'].append(result)
            if 'error' in result:break
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('days',type=int,nargs='*',default=PENDING)
    parser.add_argument('--full',action='store_true')
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--mode',choices=('student','solution'),help=argparse.SUPPRESS)
    args=parser.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    if args.mode:
        if os.environ.get("HK_COURSE_OFFLINE") == "1":
            os.environ["PYTHON_DOTENV_DISABLED"] = "1"
            os.environ.pop("OPENAI_API_KEY", None)
        day, = args.days
        r = run(day, args.mode == "solution", args.full)
        last = r["cells"][-1]
        (args.out/f"{day:02}-{args.mode}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2))
        if "error" in last:
            print(last["error"],flush=True)
        print(day,args.mode,len(r["cells"]),last["id"],"ERROR" if "error" in last else "OK",flush=True)
        raise SystemExit(int("error" in last))
    failed = []
    for day in args.days:
        for mode in ("student","solution"):
            cmd = [sys.executable,__file__,"--out",str(args.out.resolve()),"--mode",mode,str(day)]
            if args.full:
                cmd.append("--full")
            if subprocess.run(cmd).returncode:
                failed.append((day,mode))
    if failed:
        raise SystemExit(str(failed))
