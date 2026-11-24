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
        self.links = []
        self.notebooks = []
        self.simulations = []
        self.has_practice = False
        self.has_clip = False
        self.clip_playback_errors = []
        self.title = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "xlink:href", "src", "srcset", "poster", "data-gif", "data-still", "data-sheet"):
            value = attrs.get(key)
            if not value or value.startswith("data:"):
                continue
            if key == "srcset":
                self.links.extend(item.split()[0] for item in value.split(",") if item.strip())
            else:
                self.links.append(value)
        self.has_practice |= "data-practice" in attrs
        if tag == "video" and attrs.get("src") == "concept.mp4":
            self.has_clip = True
            if not {"autoplay", "loop", "muted", "playsinline"}.issubset(attrs) or "controls" in attrs:
                self.clip_playback_errors.append("개념 영상의 무음 자동 반복 재생 설정 오류")
        if tag == "a" and attrs.get("href", "").endswith(".ipynb"):
            self.notebooks.append(attrs["href"])
        if tag == "iframe" and attrs.get("src") == "simulation.html":
            self.simulations.append(attrs["src"])


def main():
    pages = {}
    errors = []
    for path in sorted(ROOT.rglob("*.html")):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
    for path, page in pages.items():
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in page.clip_playback_errors)
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
    home = set(pages[ROOT / "index.html"].links)
    for day in range(1, 117):
        name = f"chapter{day:02d}"
        route = f"{name}/index.html"
        if route not in home:
            errors.append(f"목차에서 {route} 누락")
        page = pages[ROOT / route]
        if f"{name}.ipynb" not in page.notebooks:
            errors.append(f"{name} 노트북 링크 누락")
        notebook = json.loads((ROOT / name / f"{name}.ipynb").read_text())
        for present, asset in ((page.has_practice, "../assets/practice-space.js"), (page.has_clip, "concept.mp4")):
            if present and asset not in page.links:
                errors.append(f"{name} 새 학습 자료 연결 누락: {asset}")
        for asset in page.links:
            if asset.endswith((".svg", ".gif")) or asset == "simulation.html" or asset.startswith("motion/"):
                errors.append(f"{name} 이전 시각 자료 연결: {asset}")
        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue
            references = set(re.findall(r"attachment:([^\s)]+)", "".join(cell["source"])))
            missing = references - cell.get("attachments", {}).keys()
            if missing:
                errors.append(f"{name} 노트북 첨부 누락 {sorted(missing)}")
        if not any(cell["cell_type"] == "code" for cell in notebook["cells"]):
            errors.append(f"{name} 코드 셀 누락")
    if errors:
        raise SystemExit("\n".join(sorted(set(errors))))
    print(f"HTML {len(pages)}개, 교재·노트북 116쌍, Three.js 실험 {sum(p.has_practice for p in pages.values())}곳, 개념 영상 {sum(p.has_clip for p in pages.values())}편 통과")


if __name__ == "__main__":
    main()
