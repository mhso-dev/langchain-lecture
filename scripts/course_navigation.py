"""Use the approved timetable for chapter navigation, catalog and field activities."""
from html import escape
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1])
schedule = (ROOT / "curriculum.md").read_text().split("## 일차별 수업과 결과물", 1)[1]
groups = []
days = {}
for line in schedule.splitlines():
    group = re.fullmatch(r"### (\d+)–(\d+)일 · (.*?) · (\d+)시간", line)
    if group:
        first, last, name, hours = group.groups()
        first, last = int(first), int(last)
        assert int(hours) == (last - first + 1) * 8
        groups.append((first, last, name))
    row = re.fullmatch(r"\| (\d+) \| (.*?) \| (.*?) \|", line)
    if row:
        day, title, goal = row.groups()
        assert int(day) not in days
        days[int(day)] = (escape(title), escape(goal))
assert list(days) == list(range(1, 121))
assert [n for start, end, _ in groups for n in range(start, end + 1)] == list(days)

def route(day):
    return f"chapter{day:02}/index.html"

def adjacent(day):
    links = []
    if day > 1:
        links.append(f'<a rel="prev" href="../{route(day-1)}" aria-label="이전 일차 · {day-1}일차">← 이전</a>')
    if day < len(days):
        links.append(f'<a rel="next" href="../{route(day+1)}" aria-label="다음 일차 · {day+1}일차">다음 →</a>')
    return " ".join(links)

def chooser(day):
    sections = []
    for first, last, name in groups:
        items = []
        for n in range(first, last+1):
            current = ' aria-current="page"' if n == day else ''
            items.append(f'<a href="../{route(n)}"{current}><b>{n}일</b> {days[n][0]}</a>')
        sections.append(f'<section><h3>{first}–{last}일 · {escape(name)}</h3>{"".join(items)}</section>')
    return '<details class="day-picker"><summary>일차 선택</summary><div class="day-list">' + ''.join(sections) + '</div></details>'

for day, (title, goal) in days.items():
    file = OUT/route(day)
    if day >= 117:
        work = file.read_text()
        file.write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{day}일차 · {title}</title><link rel="stylesheet" href="../assets/catalog.css"><link rel="stylesheet" href="../assets/course-nav.css"></head><body><!-- COURSE_NAV --><header><p>특강·현장실습 · {day}일차</p><h1>{title}</h1><p>{goal}</p></header><main id="main">{work}</main></body></html>')
    page = file.read_text()
    assert page.count("<!-- COURSE_NAV -->") == 1, file
    nav = f'<nav id="course-days" class="course-nav" aria-label="일차별 교재"><a href="../index.html">교재 홈</a><span>{day}일차</span>{chooser(day)}{adjacent(day)}</nav>'
    page = page.replace("<!-- COURSE_NAV -->", nav)
    page = page.replace("</main>", f'<nav class="day-footer" aria-label="본문 끝 일차 이동">{adjacent(day)} <a href="../index.html">교재 홈</a> <a href="#course-days">일차 선택 ↑</a></nav></main>', 1)
    file.write_text(page)

catalog = OUT/"index.html"
source = catalog.read_text()
cards = {int(day): card for card,day in re.findall(r'(<article class="card"[^>]*>\s*<a href="chapter(\d+)/index.html">.*?</article>)',source,re.S)}
assert set(cards) == set(range(1,117))
units = []
for first,last,name in groups:
    unit = []
    for n in range(first,last+1):
        title,goal = days[n]
        if n in cards:
            card=cards[n]
            # The schedule is the visible heading. Keep searches for unchanged lesson terminology.
            old = re.search(r'data-search="([^"]*)"',card)[1] if not 81<=n<=85 else ""
            card=re.sub(r'data-search="[^"]*"',lambda _:f'data-search="{n}일차 {title} {old}"',card)
            card=re.sub(r'<h3>.*?</h3>',lambda _:f'<h3>{title}</h3>',card)
            if 81<=n<=85:
                card=re.sub(r'<span class="state [^"]+">[^<]+</span>','',card)
        else:
            card=f'<article class="card" data-search="{n}일차 {title}"><a href="{route(n)}"><span class="day">{n}일차 · 8H</span><h3>{title}</h3><span class="open">현장 활동 열기 →</span></a></article>'
        unit.append(card)
    attr=" data-project" if first in (43,86) else ""
    units.append(f'<section class="unit"{attr}><h2>{first}–{last}일 · {escape(name)}</h2><div class="grid">{"".join(unit)}</div></section>')
first_unit = source.index('<section class="unit"')
last_unit = source.rindex('</section>') + len('</section>')
source = source[:first_unit] + ''.join(units) + source[last_unit:]
source=source.replace('id="projects" type="checkbox"', 'id="projects" type="checkbox" checked').replace('일반 수업 75장 · 1–42장, 53–85장','120일 · 일반 수업 75일 · 중간 프로젝트 10일 · 최종 프로젝트 31일 · 특강·현장실습 4일')
catalog.write_text(source)
updates=OUT/"updates/index.html"
old=updates.read_text()
# Old release notes link to the preserved edition when they cite retired content.
for day in range(81,86):
    archive=OUT/f'codex{day}/index.html'
    def historical(m):
        anchor=m[1] or ""
        if not anchor or f'id="{anchor[1:]}"' in archive.read_text():
            return f'../codex{day}/index.html'+anchor
        return f'../chapter80/index.html#daily-lab'
    old=re.sub(rf'../chapter{day}/index\.html(#[\w-]+)?',historical,old)
index=''.join(f'<li><a href="../{route(n)}#course-days">{n}일 · {days[n][0]}</a></li>' for n in days)
updates.write_text(old.replace('<main>',f'<main><section id="curriculum-nov26"><h2>11월 26일 · 개편 수업표와 일차 이동</h2><p>80일차에는 투두 앱을 완성하고, 81~85일차에는 LangSmith로 추적·평가·배포 판단을 실습합니다. 각 페이지 상단에서 다른 일차를 선택할 수 있습니다.</p><details><summary>120일 교재 목록</summary><ul>{index}</ul></details></section>',1))
