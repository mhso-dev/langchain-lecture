"""Insert generated media beside its lesson in both editions without changing code cells."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import base64
from html import escape, unescape
import json
from pathlib import Path
import re
import shutil
from importlib import import_module
from scenes import SCENES
from labs import LABS

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://langchain-lecture.vercel.app'
SITE = ROOT / 'site'
SCRIPTS = '<script defer src="../assets/three.min.js"></script><script defer src="../assets/practice-space.js"></script>'


def options(lab):
    values = lab['values']
    if isinstance(values, tuple):
        low, high, step, start = values
        return f'<input type="range" min="{low}" max="{high}" step="{step}" value="{start}"><span class="practice-value">{start}</span>'
    return '<select>'+''.join(f'<option value="{escape(v)}">{escape(label)}</option>' for v,label in values)+'</select>'


def add(day, spec, ident, media=None):
    name = f'chapter{day:02d}'
    folder = SITE / name
    page = folder / 'index.html'
    book = folder / f'{name}.ipynb'
    source = page.read_text()
    notebook = json.loads(book.read_text())
    anchor = spec['section']
    section = re.search(r'<section id="'+re.escape(anchor)+r'" class="lesson-section">.*?(?=<section id="|</main>)',source,re.S)
    if not section:
        raise ValueError(f'{name}: section {anchor} missing')
    title = escape(spec['title'])
    caption = spec['caption'] if media else spec['observation']
    if media:
        mp4 = ident+'.mp4'
        shutil.copyfile(media.with_suffix('.mp4'),folder/mp4)
        figure=(f'<figure class="lesson-clip" id="{ident}"><h3>{title}</h3>\n'
                f'<video autoplay loop muted playsinline aria-label="{title}" src="{mp4}"></video>\n'
                f'<figcaption>{escape(caption)}</figcaption></figure>')
    else:
        figure=(f'<section class="practice-space" id="{ident}" data-practice="{spec["key"]}"><h3>{title}</h3>'
                f'<p>{escape(spec["question"])}</p><label>{escape(spec["control"])} {options(spec)}</label>'
                f'<div class="practice-stage" role="img" aria-label="{title}"></div><output aria-live="polite">{escape(caption)}</output></section>')
    begin = f'<!-- lesson-visual {ident} -->'
    end = f'<!-- /lesson-visual {ident} -->'
    pattern = re.escape(begin)+'.*?'+re.escape(end)
    block = begin+'\n'+figure+'\n'+end
    if begin in source:
        source = re.sub(pattern,lambda _:block,source,count=1,flags=re.S)
    else:
        before = section.group().find('<article class="notebook-cell"')
        if before<0: raise ValueError(f'{name}: missing cell in {anchor}')
        at = section.start()+before
        source = source[:at]+block+'\n'+source[at:]
    if not media and '../assets/practice-space.js' not in source:
        source = source.replace('</head>',SCRIPTS+'</head>',1)
    section_title = unescape(re.search(r'<h2[^>]*>(.*?)</h2>',section.group(),re.S)[1])
    cell = next(c for c in notebook['cells'] if c['cell_type']=='markdown' and ''.join(c['source']).splitlines()[0].strip()=='## '+section_title)
    md = f'**{spec["title"]}**\n\n'
    if media:
        attachment = ident+'.gif'
        md+=f'![{spec["title"]}](attachment:{attachment})\n\n'
        cell.setdefault('attachments',{})[attachment]={'image/gif':base64.b64encode(media.with_suffix('.gif').read_bytes()).decode()}
    else:
        md+=spec['question']+'\n\n'
    md+=caption
    if not media: md+=f'\n\n[웹 교재에서 직접 조작하기]({BASE}/{name}/#{ident})'
    cell_text=''.join(cell['source'])
    span=begin+'\n'+md+'\n'+end
    updated=re.sub(pattern,lambda _:span,cell_text,flags=re.S) if begin in cell_text else cell_text.rstrip()+'\n\n'+span+'\n'
    cell['source']=updated.splitlines(keepends=True)
    book.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n')
    page.write_text(source)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('media',type=Path)
    p.add_argument('--extras-only',action='store_true')
    p.add_argument('--base-only',action='store_true')
    args=p.parse_args()
    extras = {}
    for path in sorted(Path(__file__).parent.glob('extra_*.py')):
        extras.update(import_module(path.stem).EXTRAS)

    def integrate_chapter(day):
        if not args.extras_only:
            if day in SCENES:
                spec = SCENES[day]
                add(day, spec, 'visual-'+spec['section'][3:], args.media/f'chapter{day:02}')
            if day in LABS:
                add(day, LABS[day], 'practice-space')
        if not args.base_only and day in extras:
            spec = extras[day]
            add(day, spec, 'detail-'+spec['section'][3:], args.media/f'extra{day:02}')

    with ThreadPoolExecutor(max_workers=8) as workers:
        list(workers.map(integrate_chapter, range(1,117)))
