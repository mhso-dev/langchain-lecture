"""Publish the project chapters as worked references without separate student exercises."""
import json
import re
from html import escape

def project_reference(chapter, encode):
    notebook=chapter/(chapter.name+'.ipynb')
    obj=json.loads(notebook.read_bytes())
    cells=[]
    in_workshop=False
    task=False
    keep_note=''
    for item in obj['cells']:
        key=item['id']
        source=''.join(item['source'])
        if key=='workshop':
            in_workshop=True
        if key=='recap':
            in_workshop=False
            task=False
        if in_workshop:
            if key=='workshop-check':
                keep_note=source
            continue
        if key.startswith('prompt-'):
            task='과제 ' in source.splitlines()[0] or '선택 연습' in source.splitlines()[0]
        if task and (key.startswith(('prompt-','code-','notes-','answer-'))):
            continue
        if key=='recap':
            if keep_note:
                cells.append(dict(cell_type='markdown',metadata={},id='project-note',source=['### 프로젝트 판단 기준\n\n'+keep_note]))
            item['source']=source.replace('## 돌아보기','## 프로젝트 인계 기준').splitlines(keepends=True)
        cells.append(item)
    obj['cells']=cells
    notebook.write_bytes(encode(obj))
    page=chapter/'index.html'
    content=page.read_text()
    content=re.sub(r'<article\b[^>]*\bdata-task="1"[^>]*>.*?</article>','',content,flags=re.S)
    start=content.index('<section id="workshop"')
    end=content.index('<section id="recap"',start)
    title=re.search(r'<h2>(.+?)</h2>',content[start:end],re.S).group(1)
    note=keep_note if keep_note else '이 장의 본문 사례를 팀의 설계와 인계 기준에 참고합니다.'
    content=content[:start]+'<section id="workshop" class="lesson-section"><h2>프로젝트 판단 기준</h2><p>'+note+'</p></section>'+content[end:]
    content=content.replace(title,'프로젝트 판단 기준').replace('적용 과제와 인계 기준','프로젝트 인계 기준').replace('실습 노트북과 실행 환경','프로젝트 참고 노트북').replace('수업 노트북 (.ipynb)','프로젝트 참고 노트북 (.ipynb)')
    page.write_text(content)
