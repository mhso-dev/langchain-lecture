"""Run the notebook and its published answers in fresh kernels; inspect the actual PDF and ZIP.

Authoring environment: Python 3.12, ipykernel, nbformat, langchain-core 1.6.12,
pypdf 6.21.4 and PyMuPDF. Run from any working directory with
python scripts/check_chapter20.py. Student files are read-only.
"""
import base64
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

import nbformat
import pymupdf
from ipykernel.inprocess.manager import InProcessKernelManager
from pypdf import PdfReader

SITE = Path(__file__).resolve().parents[1] / "site" / "chapter20"
INPUTS = ("library.txt", "library-guide.pdf", "return-notice.pdf", "desk-change.txt")
GUIDE = (
    "도서 대출 기간은 14일입니다.",
    "도서관은 월요일에 휴관합니다.",
    "무인 반납함은 24시간 이용할 수 있습니다.",
)


def stdout(cell):
    return "".join(output.text for output in cell.outputs if output.output_type == "stream").rstrip("\n")


def run_cells(notebook, directory):
    os.chdir(directory)
    manager = InProcessKernelManager()
    manager.start_kernel()
    client = manager.client()
    client.start_channels()
    try:
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            message = client.execute(cell.source)
            reply = client.get_shell_msg(timeout=30)["content"]
            assert reply["status"] == "ok", (cell.id, reply)
            cell.outputs = []
            while True:
                msg = client.get_iopub_msg(timeout=30)
                if msg["parent_header"].get("msg_id") not in (message, None):
                    continue
                kind, content = msg["header"]["msg_type"], msg["content"]
                if kind == "status" and content["execution_state"] == "idle":
                    break
                if kind in ("stream", "display_data", "execute_result", "error"):
                    cell.outputs.append(nbformat.v4.new_output(kind, **content))
    finally:
        client.stop_channels()
        manager.shutdown_kernel()


def check_execution(mode):
    notebook = nbformat.read(SITE / "chapter20.ipynb", as_version=4)
    nbformat.validate(notebook)
    stored = {c.id: stdout(c) for c in notebook.cells if c.cell_type == "code"}
    body = (SITE / "index.html").read_text(encoding="utf-8")
    articles = re.findall(r'<article class="notebook-cell" data-cell="(\d+)" data-task="([01])">(.*?)</article>', body, re.S)
    expected = {}
    cells = {c.id: c for c in notebook.cells}
    for number, is_task, article in articles:
        cell_id = "code-" + number
        plain_output = re.search(r'<div class="output">.*?<pre[^>]*>(.*?)</pre>', article, re.S)
        expected[cell_id] = html.unescape(plain_output[1]) if mode == "solutions" or is_task == "0" else ""
        if is_task == "1":
            answer = re.search(r"<pre><code>(.*?)</code></pre>", cells["answer-" + number].source, re.S)
            if mode == "solutions":
                cells[cell_id].source = html.unescape(answer[1])
    assert set(expected) == set(stored) - {"fixtures"}
    with tempfile.TemporaryDirectory() as folder:
        directory = Path(folder)
        if mode == "starter":
            shutil.copy(SITE / "chapter20.ipynb", directory / "도서관-실습.ipynb")
            (directory / "chapter20-old.ipynb").write_text('{"metadata":{"library_lesson_20_inputs_v1":"OLD"}}')
        else:
            for name in INPUTS:
                shutil.copy(SITE / name, directory / name)
        before = Path.cwd()
        try:
            run_cells(notebook, directory)
        finally:
            os.chdir(before)
        for cell_id, text in expected.items():
            assert stdout(cells[cell_id]) == text, (mode, cell_id, stdout(cells[cell_id]), text)
            if mode == "starter":
                assert stored[cell_id] == text, (mode, cell_id, "stored output")
        assert stdout(cells["fixtures"]) == ", ".join(INPUTS)
        if mode == "solutions":
            handoff = json.loads((directory / "chapter20-output" / "desk-handoff.json").read_text(encoding="utf-8"))
            assert handoff["documents"] == [{"id": "desk-1", "text": "분실물은 2층 안내 데스크에 맡겨 주세요.", "source": "desk-change.txt", "page": None}]
            assert handoff["questions"][0]["expected_document_ids"] == ["desk-1"]
            assert handoff["questions"][1]["answerable"] is False
    print(f"{mode}: {len(stored)} cells; {len(expected)} HTML outputs checked")


def main():
    if len(sys.argv) == 2 and sys.argv[1] in ("starter", "solutions"):
        check_execution(sys.argv[1])
        return
    notebook = nbformat.read(SITE / "chapter20.ipynb", as_version=4)
    embedded = base64.b64decode(notebook.metadata["library_lesson_20_inputs_v1"])
    with ZipFile(io.BytesIO(embedded)) as inputs, ZipFile(SITE / "chapter20-lab.zip") as bundle:
        assert set(inputs.namelist()) == set(INPUTS)
        assert set(bundle.namelist()) == set(INPUTS) | {"chapter20.ipynb"}
        for name in INPUTS:
            assert inputs.read(name) == bundle.read(name) == (SITE / name).read_bytes(), name
        assert bundle.read("chapter20.ipynb") == (SITE / "chapter20.ipynb").read_bytes()
    guide = PdfReader(SITE / "library-guide.pdf")
    assert tuple(p.extract_text().strip() for p in guide.pages) == GUIDE
    comparison = PdfReader(SITE / "return-notice.pdf")
    assert [p.extract_text().strip() for p in comparison.pages] == ["가상 도서관 반납 안내\n" + GUIDE[-1], ""]
    with pymupdf.open(SITE / "return-notice.pdf") as pdf:
        raster = [page.get_pixmap(matrix=pymupdf.Matrix(2, 2)) for page in pdf]
        preview = pymupdf.Pixmap(str(SITE / "notice-page.png"))
        assert raster[0].samples == raster[1].samples == preview.samples
    print("ZIP, embedded files, PDF text and both page images checked", flush=True)
    for mode in ("starter", "solutions"):
        subprocess.run([sys.executable, __file__, mode], check=True)


if __name__ == "__main__":
    main()
