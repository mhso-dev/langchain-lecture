"""Place integrated examples in their opening chapters and preserve old bookmarks."""
from html import escape
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


def chapter_route(n):
    return f'chapter{n:02}/index.html'


def notebook_body(book):
    parts, anchors = [], []
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
                    level = min(6, 1 + len(paragraph) - len(paragraph.lstrip('#')))
                    key = 'integrated-' + cell['id']
                    parts.append(f'<h{level} id="{key}">{escape(heading)}</h{level}>')
                    anchors.append(cell["id"])
                elif paragraph.strip():
                    parts.append('<p>'+escape(paragraph)+'</p>')
    return ''.join(parts), anchors


def redirect_page(target, script):
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>교재로 이동</title>'
            f'<script>{script}</script><noscript><meta http-equiv="refresh" content="0;url={target}"></noscript>'
            f'</head><body><a href="{target}">교재 열기</a></body></html>')


changes = []
for unit in units:
    slug, title = unit['slug'], escape(unit['title'])
    days = unit['lessons']
    route = chapter_route(days[0])
    for day in days:
        path = OUT / chapter_route(day)
        chapter = path.read_text()
        chapter = chapter.replace(f'<span>{day}일차</span>', f'<span>자료 {day}</span>')
        if 'sections' not in unit:
            chapter = re.sub(r'<span>교육일\s*\d+\s*·\s*(?:8H|8시간)</span>', '', chapter)
            chapter = chapter.replace('<span>8H · Jev 선택 실습 2H</span>', '<span>Jev 선택 실습</span>')
            chapter = re.sub(r'<p>LangSmith 기반 LLMOps · \d+일차 · 8시간</p>', '<p>LangSmith 기반 LLMOps</p>', chapter)
        path.write_text(chapter)
    path = OUT / route
    legacy = OUT / 'topics' / slug
    legacy.mkdir(parents=True, exist_ok=True)
    download = ''
    if 'sections' in unit:
        body = ''
        anchors = []
        for number, (label, *paras) in enumerate(unit['sections'], 1):
            key = f'case-{number}'
            anchors.append(key)
            body += f'<h3 id="integrated-{key}">{escape(label)}</h3>'
            body += ''.join(f'<p>{escape(para)}</p>' for para in paras)
    else:
        notebook = BOOK / (slug + '.ipynb')
        body, anchors = notebook_body(json.loads(notebook.read_text()))
        for directory in (path.parent, legacy):
            shutil.copyfile(notebook, directory / notebook.name)
        download = f'<p><a href="{notebook.name}" download>통합 실습 노트북 받기</a></p>'

    section = (f'<section class="lesson-section" id="integrated-example"><h2>{title}</h2>'
               f'<p>{escape(unit["lead"])}</p>{download}{body}</section>')
    content = path.read_text()
    # Insert before the end controls, including fieldwork chapters without a lesson footer.
    marker = '<footer class="lesson-footer">' if '<footer class="lesson-footer">' in content else '<nav class="day-footer"'
    if marker not in content:
        raise ValueError(f'{route}: 교재 끝 이동 영역이 없습니다')
    content = content.replace(marker, section + marker, 1)
    if 'data-workflow' in body and '../assets/workflows.js' not in content:
        content = content.replace('</head>', '<script defer src="../assets/mermaid/mermaid.tiny.js"></script>'
                                  '<script defer src="../assets/workflows.js"></script></head>', 1)
    # A direct link near the introduction makes the additional material discoverable.
    jump = f'<p class="integrated-jump"><a href="#integrated-example">{title} · {("프로젝트 안내" if "sections" in unit else "통합 실습")}</a></p>'
    content = re.sub(r'</h1>', lambda m: m[0]+jump, content, count=1)
    path.write_text(content)

    target = '../../' + route + '#integrated-example'
    script = (f'const anchors={json.dumps(anchors)}, days={json.dumps(days)};'
              'const key=location.hash.slice(1);const match=/^material-(\\d+)$/.exec(key);'
              'const day=match && Number(match[1]);'
              'if(days.includes(day)){location.replace("../../chapter"+String(day).padStart(2,"0")+"/index.html");}'
              f'else{{location.replace("../../{route}#"+(anchors.includes(key)?"integrated-"+key:"integrated-example"));}}')
    (legacy/'index.html').write_text(redirect_page(target, script))
    changes.append(f'<li><a href="../{route}#integrated-example">{days[0]}장 · {title}</a></li>')

# The curriculum build already groups all 120 chapters by subject on the home page.
catalog = OUT / 'index.html'
home = re.sub(r'<span class="state [^"]+">[^<]*</span>', '', catalog.read_text())
home = home.replace('#curriculum-nov26">11월 26일 개편 수업표와 장별 변경 내역',
                    '#topic-edition">교재 개정 내역과 통합 실습')
catalog.write_text(home)
(OUT / 'schedule.html').write_text(redirect_page('index.html', 'location.replace("index.html"+location.hash)'))
updates = OUT / 'updates/index.html'
updates.write_text(updates.read_text().replace('<main>', '<main><section id="topic-edition"><h2>11월 26일 · 일차 교재에서 바로 읽는 통합 실습</h2>'
    '<p>홈에서 1~120일 교재를 바로 엽니다. 아래 장에는 통합 예제와 노트북 또는 프로젝트 안내가 수록되어 있습니다.</p><ul>'
    + ''.join(changes) + '</ul></section>', 1))

# Older editions and companion pages use different labels for the same home page.
for extra in [OUT / name / 'index.html' for name in ('execution', 'updates')] + sorted(OUT.glob('codex*/index.html')):
    content, count = re.subn(r'(<a\b[^>]*href="\.\./index\.html"[^>]*>)(?:← )?전체 (?:교재|목차)(</a>)', r'\g<1>교재 홈\2', extra.read_text())
    if not count:
        raise ValueError(f'{extra}: 교재 홈 링크 누락')
    extra.write_text(content)

practice_links = ''.join(f'<li><a href="../chapter{day:02}/index.html#applied-clinic">{day}일 · {escape(title)}</a></li>'
                         for day, title in [(75,"복구 검사"),(76,"실패 테스트"),(77,"배포 조건"),(78,"화면 상태"),(79,"API 연동"),(80,"변경 요청 인수 시험")])
updates.write_text(updates.read_text().replace('<main>', '<main><section id="live-practice"><h2>실제 모델 호출과 확장 실습</h2>'
    '<p><a href="../chapter62/index.html#workshop">MCP 조회와 실제 모델 연결</a> · <a href="../index.html">실습이 포함된 일차별 교재</a></p>'
    '<h3>Codex로 이어 만드는 서비스</h3><ul>'+practice_links+'</ul></section>',1))

# Keep bookmarks from the retired exercise index working without a separate reader.
(OUT/'daily/index.html').write_text(r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>교재로 이동</title>
<script>const day = /^#day(\d{1,3})$/.exec(location.hash);const n = day ? Number(day[1]) : 0;
const anchor = (n >= 43 && n <= 52 || n >= 86 && n <= 116) ? "applied-clinic" : "daily-lab";
location.replace(n >= 1 && n <= 120 ? "../chapter"+String(n).padStart(2,"0")+"/index.html#"+anchor : "../index.html");</script>
<noscript><meta http-equiv="refresh" content="0;url=../index.html"></noscript></head><body><a href="../index.html">일차별 교재로 이동</a></body></html>""")
