"""Publish the topic-based reader alongside the optional timetable."""
from html import escape, unescape
from pathlib import Path
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coursebook"
OUT = Path(sys.argv[1])
units = json.loads((BOOK / "units.json").read_text())
order = [day for unit in units for day in unit["lessons"]]
if order != list(range(1, 121)):
    raise ValueError("단원별 자료 목록에서 중복되거나 빠진 교육일이 있습니다.")


def plain(markup):
    return unescape(re.sub("<[^>]+>", "", markup)).strip()


def page(title, body, prefix, scripts=""):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)} · LLM 실습 교재</title><link rel="stylesheet" href="{prefix}assets/topic-reader.css">'
            f'{scripts}</head><body><a class="skip" href="#main">본문으로</a>{body}</body></html>')


def chapter_route(n):
    return f'chapter{n:02}/index.html'


def notebook_body(book):
    parts, toc = [], []
    for cell in book["cells"][1:]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code":
            parts.append('<pre class="code"><code>'+escape(source)+'</code></pre>')
            for output in cell["outputs"]:
                out = "".join(output.get("text", [])).rstrip()
                if out:
                    parts.append('<div class="output"><small>실행 결과</small><pre>'+escape(out)+'</pre></div>')
        elif source.startswith('<details class="notebook-answer">'):
            parts.append(source)
        else:
            for paragraph in source.split('\n\n'):
                if paragraph.startswith('```mermaid'):
                    chart = paragraph.split('\n', 1)[1].rsplit('\n```', 1)[0]
                    if '<' in chart:
                        raise ValueError('허용하지 않는 도식 문자')
                    parts.append('<figure data-workflow><h3>검색과 종료 경로</h3><div class="workflow-view" hidden></div>'
                                 '<script type="text/plain">'+chart+'</script></figure>')
                elif paragraph.startswith('%pip install '):
                    parts.append('<pre class="code"><code>'+escape(paragraph)+'</code></pre>')
                elif paragraph.startswith('#'):
                    heading = paragraph.lstrip('# ').strip()
                    level = len(paragraph)-len(paragraph.lstrip('#'))
                    key = cell['id']
                    parts.append(f'<h{level} id="{key}">{escape(heading)}</h{level}>')
                    if level == 2:
                        toc.append((key, heading))
                elif paragraph.strip():
                    parts.append('<p>'+escape(paragraph)+'</p>')
    return ''.join(parts), toc


def guide_links(n, full):
    labels = []
    skip = {'start', 'sources', 'recap', 'plan'}
    for anchor, title in re.findall(r'<section\b[^>]*?\bid="([^"]+)"[^>]*>(?:(?!</section>).)*?<h2[^>]*>(.*?)</h2>', full, re.S):
        if anchor not in skip and plain(title):
            labels.append((anchor, plain(title)))
    return labels


project_slugs = {'rag-studio', 'capstone', 'field-notes'}
all_cards = []
units_folder = OUT / 'topics'
units_folder.mkdir(exist_ok=True)
for unit in units:
    slug, title, lead = (unit[k] for k in ('slug', 'title', 'lead'))
    folder = units_folder / slug
    folder.mkdir(exist_ok=True)
    is_studio = slug in project_slugs
    notebook = BOOK / (slug+'.ipynb')
    action = ''
    if is_studio:
        parts, toc = [], []
        for i, (label, *paras) in enumerate(unit['sections'], 1):
            key = f'case-{i}'
            toc.append((key, label))
            parts.append(f'<h2 id="{key}">{escape(label)}</h2>'+''.join(f'<p>{escape(p)}</p>' for p in paras))
        body = ''.join(parts)
    else:
        book = json.loads(notebook.read_text())
        body, toc = notebook_body(book)
        shutil.copyfile(notebook, folder/notebook.name)
        action = f'<a class="primary" href="{slug}.ipynb" download>통합 실습 노트북 받기 ↓</a>'

    readings, search_terms = [], [title, lead]
    for n in unit['lessons']:
        route = chapter_route(n)
        path = OUT / route
        content = path.read_text()
        name = plain(re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S)[1])
        targets = guide_links(n, content)
        if is_studio:
            targets = [(key, label) for key, label in targets if key != 'workshop']
        search_terms += [str(n), name, *(label for _, label in targets)]
        links = ''.join(f'<li><a href="../../{route}#{escape(key)}">{escape(label)}</a></li>' for key, label in targets)
        lab = json.loads((OUT/'daily'/f'day{n:03}.ipynb').read_text())
        prompts = {c['id']: ''.join(c['source']) for c in lab['cells'] if c['cell_type'] == 'markdown'}
        if 'clinic-brief' in prompts:
            exercise = prompts['clinic-brief'].split('\n\n')[3]
        else:
            exercise = prompts['solo-part-a'].split('\n\n', 1)[1]
        inline_task = f'<p><strong>직접 해보기</strong> {escape(exercise)}</p>'
        readings.append(f'<article class="reading" id="material-{n}"><h3><a href="../../{route}">{escape(name)}</a></h3>{inline_task}<ul>{links}</ul></article>')
        # Show its wider learning context at the normal entry point of every resource.
        crumb = (f'<aside class="unit-crumb" aria-label="관련 단원"><a href="../topics/{slug}/index.html">'
                 f'{escape(title)} · 단원 본문</a><a href="../topics/{slug}/index.html#material-{n}">함께 읽을 자료</a></aside>')
        content = re.sub(r'(<main\b[^>]*>)', lambda m:m[1]+crumb, content, count=1)
        content = content.replace(f'<span>{n}일차</span>',f'<span>자료 {n}</span>')
        if not is_studio:
            content = re.sub(r'<span>교육일\s*\d+\s*·\s*(?:8H|8시간)</span>', '', content)
            content = content.replace('<span>8H · Jev 선택 실습 2H</span>', '<span>Jev 선택 실습</span>')
            content = re.sub(r'<p>LangSmith 기반 LLMOps · \d+일차 · 8시간</p>', '<p>LangSmith 기반 LLMOps</p>', content)
        path.write_text(content)
    top = (f'<nav class="bar" aria-label="교재 탐색"><a href="../../index.html">교재 홈</a>'
           f'<a href="../../schedule.html">일차별 수업표</a></nav>')
    toc_links = ''.join(f'<li><a href="#{key}">{escape(label)}</a></li>' for key, label in toc)
    hero = f'<header><div class="wrap"><h1>{escape(title)}</h1><p>{escape(lead)}</p>{action}</div></header>'
    related = '<section id="readings"><h2>함께 읽을 자료와 연습</h2>'+''.join(readings)+'</section>'
    outline = f'<nav class="outline" aria-label="이 단원 목차"><h2>단원 목차</h2><ul>{toc_links}<li><a href="#readings">함께 읽을 자료와 연습</a></li></ul></nav>'
    foot = '<footer><a href="../../index.html">교재 홈</a></footer>'
    scripts = ''
    if 'data-workflow' in body:
        scripts = '<script defer src="../../assets/mermaid/mermaid.tiny.js"></script><script defer src="../../assets/workflows.js"></script>'
    (folder/'index.html').write_text(page(title, top+hero+f'<main id="main" class="layout">{outline}<article class="prose">{body}{related}</article></main>'+foot,'../../',scripts))
    category = '팀 프로젝트와 현장 활동' if is_studio else '학습 단원'
    lesson_numbers = ' '.join(str(n) for n in unit['lessons'])
    card = (f'<article class="topic" data-lessons="{lesson_numbers}" data-key="{escape(" ".join(search_terms),quote=True)}"><h3><a href="topics/{slug}/index.html">{escape(title)}</a></h3>'
            f'<p>{escape(lead)}</p></article>')
    all_cards.append((category, card))

catalog = OUT/'index.html'
schedule = catalog.read_text().replace('<h1>AI 엔지니어링 수업 교재</h1>', '<h1>일차별 수업표</h1>')
schedule = schedule.replace('</header>','<p><a style="color:inherit" href="index.html">교재 홈</a></p></header>', 1)
(OUT/'schedule.html').write_text(schedule)
groups = ''
for cat in ('학습 단원', '팀 프로젝트와 현장 활동'):
    cards = ''.join(card for category, card in all_cards if category == cat)
    groups += f'<section class="collection"><h2>{cat}</h2><div class="grid">{cards}</div></section>'
home = ('<nav class="bar" aria-label="교재 탐색"><a href="schedule.html">일차별 수업표</a>'
        '<a href="updates/index.html#topic-edition">개정 내역</a></nav><header><div class="wrap"><h1>LLM 개발 실습 교재</h1>'
        '<p>해결하려는 문제로 단원을 고르세요. 예제를 실행하고 입력을 바꿔 본 뒤, 더 연습하고 싶은 개념은 같은 단원의 세부 자료에서 이어 갑니다.</p></div></header>'
        '<main id="main" class="wrap catalog"><label for="topic-search">개념·도구·자료 번호로 찾기</label> '
        '<input type="search" id="topic-search" placeholder="예: add_conditional_edges"><span role="status" id="matches"></span>'
        +groups+'</main>')
catalog.write_text(page('주제별 교재',home,'','<script defer src="assets/topic-catalog.js"></script>'))
change_list = ''.join(f'<li><a href="../topics/{u["slug"]}/index.html">{escape(u["title"])}</a></li>' for u in units)
updates = OUT/'updates/index.html'
updates.write_text(updates.read_text().replace('<main>','<main><section id="topic-edition"><h2>주제별 교재와 통합 실습</h2>'
    '<p>학생용 첫 화면을 문제별 단원으로 바꾸고 관련 예제와 실습을 연결했습니다. 일차별 수업표는 별도로 열 수 있습니다.</p><ul>'+change_list+'</ul></section>',1))

# Older editions and companion pages use different labels for the same home page.
for extra in [OUT / name / 'index.html' for name in ('execution', 'updates')] + sorted(OUT.glob('codex*/index.html')):
    content, count = re.subn(r'(<a\b[^>]*href="\.\./index\.html"[^>]*>)(?:← )?전체 (?:교재|목차)(</a>)', r'\g<1>교재 홈\2', extra.read_text())
    if not count:
        raise ValueError(f'{extra}: 교재 홈 링크 누락')
    extra.write_text(content)

practice_links = ''.join(f'<li><a href="../chapter{day:02}/index.html#applied-clinic">{day}일 · {escape(title)}</a></li>'
                         for day, title in [(75,"복구 검사"),(76,"실패 테스트"),(77,"배포 조건"),(78,"화면 상태"),(79,"API 연동"),(80,"변경 요청 인수 시험")])
updates.write_text(updates.read_text().replace('<main>', '<main><section id="live-practice"><h2>실제 모델 호출과 확장 실습</h2>'
    '<p><a href="../chapter62/index.html#workshop">MCP 조회와 실제 모델 연결</a> · <a href="../schedule.html">실습이 포함된 일차별 교재</a></p>'
    '<h3>Codex로 이어 만드는 서비스</h3><ul>'+practice_links+'</ul></section>',1))

# Keep bookmarks from the retired exercise index working without a separate reader.
(OUT/'daily/index.html').write_text(r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>교재로 이동</title>
<script>const day = /^#day(\d{1,3})$/.exec(location.hash);const n = day ? Number(day[1]) : 0;
const anchor = (n >= 43 && n <= 52 || n >= 86 && n <= 116) ? "applied-clinic" : "daily-lab";
location.replace(n >= 1 && n <= 120 ? "../chapter"+String(n).padStart(2,"0")+"/index.html#"+anchor : "../schedule.html");</script>
<noscript><meta http-equiv="refresh" content="0;url=../schedule.html"></noscript></head><body><a href="../schedule.html">일차별 교재로 이동</a></body></html>""")
