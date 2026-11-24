"""Package the built classroom lessons, their notebooks and linked resources for offline reading."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile, ZIP_DEFLATED
import re

from check import Page, ROOT


def offline_indexes():
    home = (ROOT / "index.html").read_text()
    home, projects = re.subn(r'<section class="unit" data-project hidden>.*?</section>', "", home, flags=re.S)
    if projects != 2:
        raise ValueError("중간·최종 프로젝트 목차를 확인하세요.")
    home = re.sub(r'<label><input id="projects"[^>]*>[^<]*</label>', "", home)
    history = (ROOT / "updates/index.html").read_text()
    opening, body = history.split("<main>", 1)
    classroom = re.search(r'<section [^>]*id="classroom-edition"[^>]*>.*?</section>', body, re.S)
    if not classroom:
        raise ValueError("일반 수업 개정 내역이 없습니다.")
    opening = re.sub(r"<header>(.*?)</header>", lambda m: "<header>" + m[1].split("<p>")[0] + "</header>", opening, flags=re.S)
    return {"index.html": home, "updates/index.html": opening + "<main>" + classroom[0] + "</main></body></html>"}


def collect_files(indexes):
    days = [*range(1, 43), *range(53, 86)]
    files = set()
    pages = {}
    linked = set()
    for folder in [ROOT / "assets", *(ROOT / f"chapter{day:02d}" for day in days)]:
        for file in folder.rglob("*"):
            if file.is_file() and not file.name.startswith("."):
                files.add(file.relative_to(ROOT).as_posix())
    for name in sorted(files.union(indexes)):
        if name.endswith(".html"):
            page = Page()
            page.feed(indexes[name] if name in indexes else (ROOT / name).read_text())
            pages[name] = page
    for name, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = ((ROOT / name).parent / unquote(url.path)).resolve() if url.path else ROOT / name
            if target.is_dir():
                target /= "index.html"
            key = target.relative_to(ROOT).as_posix()
            if key not in files and key not in indexes:
                raise ValueError(f"{name}: {href}")
            if url.fragment and key in pages and unquote(url.fragment) not in pages[key].ids:
                raise ValueError(f"{name}: {href}")
            linked.add(key)
    return sorted(name for name in files if not name.endswith(".mp4") or name in linked)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    dest = parser.parse_args().output.resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    indexes = offline_indexes()
    files = collect_files(indexes)
    with TemporaryDirectory(dir=dest.parent) as tmp:
        archive = Path(tmp) / "classroom.zip"
        with ZipFile(archive, "w", ZIP_DEFLATED) as z:
            for name, data in indexes.items():
                z.writestr(name, data)
            for name in files:
                z.write(ROOT / name, name)
        with ZipFile(archive) as z:
            notebooks = [name for name in z.namelist() if re.fullmatch(r"chapter\d+/chapter\d+\.ipynb", name)]
            if len(notebooks) != 75 or z.testzip():
                raise ValueError("오프라인 교재 무결성 확인 실패")
        archive.replace(dest)
    print(f"일반 수업 75장과 연결 자료를 저장했습니다. {dest.name}")


if __name__ == "__main__":
    main()
