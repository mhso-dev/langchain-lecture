"""Execute team reference books independently and in order, each in a fresh Jupyter kernel."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

DAYS = (*range(43, 53), *range(86, 117))
ROOT = Path(__file__).resolve().parents[1]


def in_kernel(book_path, expected_origin):
    import nbformat
    from IPython.utils.capture import capture_output
    from ipykernel.inprocess.manager import InProcessKernelManager

    book = nbformat.read(book_path, as_version=4)
    nbformat.validate(book)
    kernel = InProcessKernelManager()
    kernel.start_kernel()
    try:
        for cell in book.cells:
            if cell.cell_type != "code":
                continue
            with capture_output() as received:
                result = kernel.kernel.shell.run_cell(cell.source, store_history=True)
            if not result.success:
                raise RuntimeError(f"{book_path.name} {cell.id}") from result.error_in_exec
            expected = "".join(
                output.text for output in cell.outputs if output.get("name") == "stdout"
            ).rstrip()
            actual = received.stdout.rstrip()
            if cell.id == "team-open":
                source, _, value = actual.partition("\n")
                assert source.startswith(expected_origin + " "), (book_path, source)
                assert value == expected.partition("\n")[2], (book_path, cell.id, actual)
            else:
                assert actual == expected, (book_path, cell.id, expected, actual)
    finally:
        kernel.shutdown_kernel()


def check(root, mode):
    with TemporaryDirectory() as temp:
        work = Path(temp)
        for n in DAYS:
            name = f"chapter{n}"
            folder = work / f"isolated-{n}" if mode == "isolated" else work
            folder.mkdir(exist_ok=True)
            src = root / name
            shutil.copyfile(src / f"{name}-start.json", folder / f"{name}-start.json")
            origin = "교재 예시" if mode == "isolated" or n in (43, 86) else "팀 기록"
            subprocess.run([sys.executable, __file__, "--one", str(src / f"{name}.ipynb"),
                            "--origin", origin], cwd=folder, check=True)
            track = "midterm" if n <= 52 else "final"
            saved = folder / "team-project" / track / f"{name}.json"
            result = json.loads(saved.read_text(encoding="utf-8"))
            if n not in (52, 116):
                following = root / f"chapter{n+1}" / f"chapter{n+1}-start.json"
                assert result == json.loads(following.read_text(encoding="utf-8")), name
            print(f"{name} {mode} OK", flush=True)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--source", choices=("dist", "site"), default="dist")
    args.add_argument("--mode", choices=("isolated", "linked", "both"), default="both")
    args.add_argument("--one", type=Path, help=argparse.SUPPRESS)
    args.add_argument("--origin", help=argparse.SUPPRESS)
    options = args.parse_args()
    if options.one:
        in_kernel(options.one, options.origin)
    else:
        for mode in (("linked", "isolated") if options.mode == "both" else (options.mode,)):
            check(ROOT / options.source, mode)
