"""Verify chapter 21 in the authoring kernel with the chapter 20 checker's dependencies.

Install langchain-text-splitters alongside the packages used by check_chapter20.py.
Run python scripts/check_chapter21.py. Each notebook runs in its own process and
temporary directory. Only the solution run reads copies of the public fixtures.
"""
import ast
import html
import json
import re
import shutil
import subprocess
import sys
from contextlib import chdir
from pathlib import Path
from tempfile import TemporaryDirectory

import nbformat
from langchain_text_splitters import RecursiveCharacterTextSplitter

from check_chapter20 import INPUTS as CHAPTER20_INPUTS
from check_chapter20 import run_cells, stdout

SITE = Path(__file__).resolve().parents[1] / "site"
CHAPTER = SITE / "chapter21"
INPUTS = ("guide-records.json", "branch-guide.txt")


def read_notebook(day):
    return nbformat.read(SITE / f"chapter{day}" / f"chapter{day}.ipynb", as_version=4)


def split_ranges(body, size, overlap):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap, add_start_index=True
    )
    ranges = []
    for piece in splitter.create_documents([body]):
        start = piece.metadata["start_index"]
        end = start + len(piece.page_content)
        assert body[start:end] == piece.page_content
        ranges.append([start, end, piece.page_content])
    return ranges


def check_handoff_and_visual():
    records = json.loads((CHAPTER / INPUTS[0]).read_text())
    # Actually run the four public lesson cells that extract and name PDF pages.
    previous = read_notebook(20)
    last = next(i for i, c in enumerate(previous.cells) if c.id == "code-4")
    probe = nbformat.v4.new_code_cell("print(json.dumps(documents))")
    previous.cells = previous.cells[:last + 1] + [probe]
    with TemporaryDirectory() as tmp:
        directory = Path(tmp)
        for name in CHAPTER20_INPUTS:
            shutil.copy(SITE / "chapter20" / name, directory / name)
        with chdir(directory):
            run_cells(previous, directory)
    assert json.loads(stdout(probe)) == records, "chapter 20 generated records"
    # Chapter 22 starts with three literal records before building its teaching vectors.
    first_code = next(c.source for c in read_notebook(22).cells if c.cell_type == "code")
    assignment = next(n for n in ast.parse(first_code).body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "documents" for t in n.targets))
    assert records == ast.literal_eval(assignment.value), "chapter 22 baseline"
    viewer = (CHAPTER / "chunk-lab.html").read_text()
    samples = json.loads(re.search(r'<script type="application/json" id="samples">(.*?)</script>',
                                  viewer, re.S)[1])
    assert set(samples) == {str(r["page"]) for r in records}
    count = ranges = 0
    for record in records:
        sample = samples[str(record["page"])]
        assert {k: sample[k] for k in record} == record
        assert sample["target"] and sample["target"] in record["text"]
        assert set(sample["runs"]) == {"0", "4", "6"}
        for overlap, saved in sample["runs"].items():
            assert saved == split_ranges(record["text"], 12, int(overlap)), (record["id"], overlap)
            count += 1
            ranges += len(saved)
    print(f"PDF pages and chapter 22 records match; viewer: {count} settings, {ranges} chunk ranges", flush=True)


def check_execution(mode):
    notebook = read_notebook(21)
    nbformat.validate(notebook)
    cells = {c.id: c for c in notebook.cells}
    body = (CHAPTER / "index.html").read_text()
    assert re.search(r'<iframe\b[^>]* src="chunk-lab\.html"', body)
    articles = re.findall(r'<article class="notebook-cell" data-cell="(\d+)" data-task="([01])">(.*?)</article>',
                          body, re.S)
    expected = {}
    task_count = 0
    for number, task, article in articles:
        cell_id = "code-" + number
        cell = cells[cell_id]
        web_code = [html.unescape(re.sub(r'<[^>]*>', '', block)) for block in re.findall(
            r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', article, re.S)]
        assert cell.source == web_code[0], (cell_id, "starter code")
        web_output = html.unescape(re.search(r'<div class="output">.*?<pre[^>]*>(.*?)</pre>', article, re.S)[1])
        starter_output = "" if task == "1" else web_output
        assert stdout(cell) == starter_output, (cell_id, "stored starter output")
        expected[cell_id] = starter_output
        if task == "1":
            assert "<details" in article
            notes = cells["notes-" + number]
            assert notebook.cells[notebook.cells.index(cell) + 1] is notes
            answer, example = [html.unescape(block) for block in re.findall(
                r'<pre><code>(.*?)</code></pre>', notes.source, re.S)]
            assert web_code == [cell.source, answer] and web_output == example, (cell_id, "published answer")
            if mode == "solutions":
                cell.source = answer
                expected[cell_id] = example
            task_count += 1
    assert expected and task_count and set(expected) == {c.id for c in notebook.cells if c.cell_type == "code"}
    # Only the checker appends this cell. It compares the notebook's actual input in both run modes.
    probe = nbformat.v4.new_code_cell("print(json.dumps([records, [p.page_content for p in branch]]))")
    notebook.cells.append(probe)
    with TemporaryDirectory() as tmp:
        directory = Path(tmp)
        if mode == "solutions":
            for name in INPUTS:
                shutil.copy(CHAPTER / name, directory / name)
        with chdir(directory):
            run_cells(notebook, directory)
        for cell_id, text in expected.items():
            assert stdout(cells[cell_id]) == text, (mode, cell_id, stdout(cells[cell_id]), text)
        records, branch_pages = json.loads(stdout(probe))
        assert records == json.loads((CHAPTER / INPUTS[0]).read_text())
        assert branch_pages == (CHAPTER / INPUTS[1]).read_text().split("\f")
        output = directory / "chapter21-output/desk-hours.json"
        if mode == "solutions":
            saved = json.loads(output.read_text())
            page = saved["page"]
            assert 1 <= page <= len(branch_pages)
            assert saved["source"] == INPUTS[1] and saved["document_id"] == f"branch-{page}"
            assert saved["id"] == f"{saved['document_id']}:{saved['start']}"
            assert (saved["chunk_size"], saved["chunk_overlap"]) == (70, 12)
            assert [saved["start"], saved["end"], saved["text"]] in split_ranges(branch_pages[page - 1], 70, 12)
        else:
            assert not output.exists(), "the unanswered task produced a handoff file"
    print(f"{mode}: {len(expected)} notebook cells and web outputs; {task_count} published solutions", flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ("starter", "solutions"):
        check_execution(sys.argv[1])
    else:
        check_handoff_and_visual()
        for mode in ("starter", "solutions"):
            subprocess.run([sys.executable, __file__, mode], check=True)
