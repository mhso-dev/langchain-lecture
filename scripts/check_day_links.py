"""Verify every timetable destination, including the project and fieldwork boundaries."""
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "dist"

class Navigation(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_nav = False
        self.in_picker = False
        self.choices = []
        self.adjacent = {}
        self.current = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "nav":
            self.in_nav = values.get("id") == "course-days"
        if not self.in_nav:
            return
        if tag == "details":
            self.in_picker = True
        if tag == "a":
            if self.in_picker:
                self.choices.append(values["href"])
            if values.get("aria-current") == "page":
                self.current.append(values["href"])
            if "rel" in values:
                self.adjacent[values["rel"]] = values["href"]

    def handle_endtag(self, tag):
        if tag == "details":
            self.in_picker = False
        if tag == "nav":
            self.in_nav = False

paths = [f"chapter{n:02}/index.html" for n in range(1,121)]
for i, path in enumerate(paths):
    nav = Navigation()
    nav.feed((ROOT/path).read_text())
    assert nav.choices == ["../" + p for p in paths], path
    assert nav.current == ["../" + path], path
    expected = {}
    if i:
        expected["prev"] = "../" + paths[i-1]
    if i+1 < len(paths):
        expected["next"] = "../" + paths[i+1]
    assert nav.adjacent == expected, path
print("120일 선택 링크 14,400개와 이전·다음 238개 일치")
