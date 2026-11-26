"""Package the built classroom lessons, their notebooks and linked resources for offline reading."""
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile, ZIP_DEFLATED
import re

from check import Page, ROOT


def offline_files():
    """Keep general units and supporting downloads, and omit links to out-of-scope lessons."""
    days = {*range(1, 43), *range(53, 86)}
    excluded_topics = {"rag-studio", "capstone", "field-notes"}
    files = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name.startswith("."):
            continue
        name = path.relative_to(ROOT)
        chapter = re.fullmatch(r"chapter(\d+)", name.parts[0])
        if chapter and int(chapter[1]) not in days:
            continue
        if name.parts[0] == "topics" and name.parts[1] in excluded_topics:
            continue
        files[name.as_posix()] = path

    indexes = {}
    pages = {}
    for name, path in files.items():
        if path.suffix != ".html":
            continue
        content = path.read_text()
        if name == "index.html":
            content = re.sub(r'<section class="collection"><h2>팀 프로젝트와 현장 활동</h2>.*?</section>', "", content, flags=re.S)
        if name == "schedule.html":
            content = re.sub(r'<section class="unit" data-project hidden>.*?</section>', "", content, flags=re.S)
            content = re.sub(r'<label><input id="projects"[^>]*>[^<]*</label>', "", content)

        def offline_link(match):
            url = urlsplit(match[1])
            if url.scheme or url.netloc or not url.path:
                return match[0]
            target = (path.parent / unquote(url.path)).resolve()
            if target.is_dir():
                target /= "index.html"
            return match[0] if target.relative_to(ROOT).as_posix() in files else ""

        content = re.sub(r'<a\b[^>]*? href="([^"]*)"[^>]*>.*?</a>', offline_link, content, flags=re.S)
        indexes[name] = content
        pages[name] = Page()
        pages[name].feed(content)

    for name, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            path = files[name]
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            key = target.relative_to(ROOT).as_posix()
            if key not in files or (url.fragment and key in pages and unquote(url.fragment) not in pages[key].ids):
                raise ValueError(f"{name}: {href}")
    return indexes, sorted(set(files) - indexes.keys())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    dest = parser.parse_args().output.resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    indexes, files = offline_files()
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
