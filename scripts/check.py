"""Check the built student site, internal links and notebooks using the standard library."""
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1] / "dist"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicate_ids = set()
        self.copy_targets = set()
        self.links = []
        self.notebooks = []
        self.old_media = []
        self.has_practice = False
        self.workflows = 0
        self.closed_lesson_blocks = []
        self.title = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "details" and "day-picker" not in attrs.get("class","").split() and not {"notebook-answer", "checkpoint"}.intersection(attrs.get("class", "").split()):
            self.closed_lesson_blocks.append(attrs.get("id", attrs.get("class", "details")))
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicate_ids.add(attrs["id"])
            self.ids.add(attrs["id"])
        if "data-copy" in attrs:
            self.copy_targets.add(attrs["data-copy"])
        for key in ("href", "xlink:href", "src", "srcset", "poster", "data-gif", "data-still", "data-sheet", "data-page-image"):
            value = attrs.get(key)
            if not value or value.startswith("data:"):
                continue
            if key == "srcset":
                self.links.extend(item.split()[0] for item in value.split(",") if item.strip())
            else:
                self.links.append(value)
        self.has_practice |= "data-practice" in attrs
        if tag in {"video", "img", "canvas"} or "three.min.js" in attrs.get("src", ""):
            self.old_media.append(tag)
        self.workflows += int("data-workflow" in attrs)
        if tag == "a" and attrs.get("href", "").endswith(".ipynb"):
            self.notebooks.append(attrs["href"])


def main():
    pages = {}
    errors = []
    for path in sorted(ROOT.rglob("*.html")):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
    for path, page in pages.items():
        if page.old_media:
            errors.append(f"{path.relative_to(ROOT)} 이전 미디어: {page.old_media}")
        for key in sorted(page.copy_targets - page.ids):
            errors.append(f"{path.relative_to(ROOT)} 코드 복사 대상 누락: {key}")
        for key in sorted(page.duplicate_ids):
            errors.append(f"{path.relative_to(ROOT)} 중복 앵커: {key}")
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f"{path.relative_to(ROOT)} -> {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(ROOT)} -> {link} (앵커 누락)")
    for file in ROOT.rglob("*"):
        if file.suffix in {".html", ".ipynb", ".py"}:
            content = file.read_text()
            if any(name in content for name in ("FakeMessagesListChatModel", "FakeListChatModel")):
                errors.append(f"{file.relative_to(ROOT)} 수업용 모델 대역이 남았습니다")
    catalog = pages[ROOT / "index.html"]
    units = json.loads((ROOT.parent / "coursebook/units.json").read_text())
    for unit in units:
        slug = unit["slug"]
        route = f"topics/{slug}/index.html"
        topic = pages[ROOT / route]
        assert route in catalog.links, route
        if "sections" not in unit:
            filename = slug + ".ipynb"
            assert filename in topic.links, filename
            assert (ROOT / "topics" / slug / filename).read_bytes() == (ROOT.parent / "coursebook" / filename).read_bytes()
        for day in unit["lessons"]:
            chapter = f"chapter{day:02}/index.html"
            assert f"../../{chapter}" in topic.links and f"material-{day}" in topic.ids, chapter
            assert f"../{route}" in pages[ROOT / chapter].links, chapter
    home = set(pages[ROOT / "schedule.html"].links)
    for day in range(1, 117):
        name = f"chapter{day:02d}"
        route = f"{name}/index.html"
        if route not in home:
            errors.append(f"목차에서 {route} 누락")
        page = pages[ROOT / route]
        if page.closed_lesson_blocks or 'href="#readings"' in (ROOT / route).read_text():
            errors.append(f"{name} 본문에 접힌 설명 또는 이전 심화 읽기 목차가 남았습니다")
        if f"{name}.ipynb" not in page.notebooks:
            errors.append(f"{name} 노트북 링크 누락")
        notebook = json.loads((ROOT / name / f"{name}.ipynb").read_text())
        if "guided-reading" not in page.ids:
            errors.append(f"{name} 핵심 해설 누락")
        if page.has_practice and "../assets/practice-space.js" not in page.links:
            errors.append(f"{name} 조작 실습 스크립트 누락")
        charts = [
            source
            for cell in notebook["cells"] if cell["cell_type"] == "markdown"
            for source in re.findall(r"^```mermaid\n(.+?)\n```", "".join(cell["source"]), re.M | re.S)
        ]
        page_text = (ROOT / route).read_text()
        web_charts = re.findall(r'<figure\b[^>]*\bdata-workflow\b[^>]*>.*?<script type="text/plain">(.*?)</script>.*?</figure>', page_text, re.S)
        if page.workflows != len(charts) or web_charts != charts:
            errors.append(f"{name} 웹·노트북 Mermaid 흐름도 원문 또는 순서 불일치")
        rendered_charts = re.findall(r'<div class="workflow-view">\s*<svg\b', page_text)
        if charts and "../assets/workflows.js" not in page.links and len(rendered_charts) != len(charts):
            errors.append(f"{name} Mermaid 스크립트 연결 누락")
        cells = notebook["cells"]
        for index, cell in enumerate(cells):
            if cell["cell_type"] == "code":
                following = index + 1
                while following < len(cells) and cells[following].get("id", "").startswith("guided-"):
                    following += 1
                if following > index + 1 and following < len(cells):
                    if "".join(cells[following]["source"]).lstrip().startswith("<details"):
                        errors.append(f"{name} 과제와 풀이 사이에 새 해설이 들어갔습니다")
            if cell["cell_type"] != "markdown":
                continue
            references = set(re.findall(r"attachment:([^\s)]+)", "".join(cell["source"])))
            if any(key != "coordinates.svg" for key in cell.get("attachments", {})):
                errors.append(f"{name} 이전 삽화 첨부")
            missing = references - cell.get("attachments", {}).keys()
            if missing:
                errors.append(f"{name} 노트북 첨부 누락 {sorted(missing)}")
        if not any(cell["cell_type"] == "code" for cell in notebook["cells"]):
            errors.append(f"{name} 코드 셀 누락")
    removed_extensions = {".mp4", ".webm", ".gif", ".png", ".jpg", ".jpeg", ".webp"}
    for asset in ROOT.rglob("*"):
        if asset.is_file() and (asset.suffix.lower() in removed_extensions or asset.name == "three.min.js"):
            errors.append(f"배포에 이전 미디어 파일 포함: {asset.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(sorted(set(errors))))
    charts = sum(p.workflows for p in pages.values())
    print(f"HTML {len(pages)}개, 교재·노트북 116쌍, Mermaid 차트 {charts}개 및 내부 링크 통과")



if __name__ == "__main__":
    main()
