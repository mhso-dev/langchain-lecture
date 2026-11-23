"""Render the selected chapters and update both student editions (Pillow required)."""
import argparse
import base64
import html
import io
import json
from pathlib import Path
import re
from concurrent.futures import ProcessPoolExecutor
from importlib import import_module
from PIL import Image
from studio import Board, SCENES, W, H

ROOT = Path(__file__).resolve().parents[1]
for module in sorted(Path(__file__).parent.glob('unit_*.py')):
    import_module(module.stem)
import_module('python_and_models')

FRAMES = 40
COLS = 5
DURATION = 5000
TINTS = ('#f5f0e5','#ecf4f3','#eff3fa','#fbf0e9')

def compile_chapter(day):
    name = f'chapter{day:02}'
    folder = ROOT/'site'/name
    page = folder/'index.html'
    book = folder/(name+'.ipynb')
    notebook = json.loads(book.read_bytes())
    source = page.read_text()
    scenes = [item for item in SCENES.values() if item.chapter == day]
    if not scenes:
        return
    for item in scenes:
        key = item.key
        target = folder/'motion'
        target.mkdir(exist_ok=True)
        marker = f'<!-- MOTION {key} -->'
        endmark = '<!-- END MOTION -->'
        source = re.sub(r'\n?'+re.escape(marker)+'.*?'+re.escape(endmark)+'\n?', '', source, flags=re.S)
        frames = []
        for index in range(FRAMES):
            b = Board(TINTS[(day-1)%len(TINTS)])
            item.draw(b,index/(FRAMES-1))
            frames.append(b.image)
        width,height = frames[0].size
        sheet = Image.new('RGB',(width*COLS,height*((FRAMES+COLS-1)//COLS)))
        for index,frame in enumerate(frames):
            sheet.paste(frame,((index%COLS)*width,(index//COLS)*height))
        sheet.save(target/(key+'.webp'),lossless=True,method=2)
        frames[-1].save(target/(key+'-still.webp'),lossless=True,method=3)
        # Preserve every character arrival for the streaming lesson.
        stride = 1 if key == 'stream-typesetter' else 2
        sample = list(range(0, FRAMES - 1, stride)) + [FRAMES - 1]
        small = [frames[i].resize((W, H), Image.Resampling.LANCZOS) for i in sample]
        binary = io.BytesIO()
        small[0].save(binary,format='GIF',save_all=True,append_images=small[1:],duration=[DURATION // FRAMES * stride]*(len(small)-1)+[1200],optimize=True)
        title,caption = map(html.escape,(item.title,item.explanation))
        readings = {
            'overlap-scissors': [('겹침 0글자',0),('겹침 2글자',19),('겹침 4글자',39)],
            'candidate-race': [('첫 검색 순위',0),('재정렬한 순위',39)],
            'memory-aperture': [('전체 4턴',0),('최근 3턴',19),('최근 2턴',39)],
            'reset-tank': [('30분 처리 뒤',10),('20분 처리 뒤',22),('40분 처리 뒤',39)],
            'baseline-error': [('기준선 보기',0),('Q03 대조',39)],
        }
        choices = ''.join(f'<button type="button" data-frame="{frame}">{label}</button>' for label,frame in readings.get(key,[]))
        choices = f'<div class="motion-choices" hidden>{choices}</div>' if choices else ''
        block = f'''{marker}
<figure class="motion-study" id="motion-{key}" data-sheet="motion/{key}.webp" data-frames="{FRAMES}" data-cols="{COLS}" data-duration="{DURATION}">
<h3>{title}</h3>
<div class="motion-viewport"><div class="motion-stage"><img loading="lazy" src="motion/{key}-still.webp" width="{width}" height="{height}" alt="{caption}"><canvas hidden width="{width}" height="{height}" aria-hidden="true"></canvas></div></div>
{choices}
<div class="motion-tools" hidden><button type="button">재생</button><label>장면 위치 <input type="range" min="0" max="{FRAMES-1}" value="0"></label><button type="button" class="motion-zoom" aria-pressed="false">크게 보기</button></div>
<figcaption>{caption}</figcaption>
</figure>
{endmark}
'''
        sections = list(re.finditer(r'<section id="([^"]+)" class="lesson-section">',source))
        section = sections[item.section]
        close = source.index('</header>',section.end())+len('</header>')
        # Let the reader encounter the example's introductory paragraph first.
        firstp = re.match(r'\s*<p(?: [^>]*)?>.*?</p>',source[close:],re.S)
        if firstp:
            close += firstp.end()
        source = source[:close]+'\n'+block+source[close:]
        cell_id = 'explanation-3' if day==12 else f'section-{item.section}'
        cell = next(c for c in notebook['cells'] if c.get('id') == cell_id)
        asset = key+'.gif'
        text = ''.join(cell['source'])
        text = re.sub(r'\n*<!-- motion:'+re.escape(key)+r' -->.*?<!-- /motion -->','',text,flags=re.S)
        text = text.rstrip()+f'\n\n<!-- motion:{key} -->\n**{item.title}**\n\n![{item.title}](attachment:{asset})\n\n{item.explanation}\n<!-- /motion -->\n'
        cell['source'] = text.splitlines(keepends=True)
        cell.setdefault('attachments',{})[asset] = {'image/gif':base64.b64encode(binary.getvalue()).decode('ascii')}
    if '../assets/motion-study.js' not in source:
        source = source.replace('</head>','<link rel="stylesheet" href="../assets/motion-study.css">\n<script defer src="../assets/motion-study.js"></script>\n</head>')
    page.write_text(source)
    book.write_text(json.dumps(notebook,ensure_ascii=False,separators=(',',':'))+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('days',type=int,nargs='*',help='chapter numbers; default: every illustrated chapter')
    args = parser.parse_args()
    days = sorted(set(args.days or [s.chapter for s in SCENES.values()]))
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(compile_chapter,days))
    print(f'Rendered {len(days)} chapters.')
