"""Rebuild this edition from the preceding site snapshot and rendered media.

Use a separate source directory. HTML outside changed fragments retains its original
spelling, including the code cells. Lesson placement is curated in unit*.py.
"""
import argparse
from base64 import b64encode
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from html import escape, unescape
from html.parser import HTMLParser
from importlib import import_module
import json
from pathlib import Path
import re
import shutil

from lxml import html as lh

ROOT=Path(__file__).resolve().parents[2]
VOID=set('area base br col embed hr img input link meta param source track wbr'.split())


@dataclass(eq=False)
class Element:
    tag:str
    attrs:dict
    start:int
    inner:int
    end:int
    close:int
    children:list=field(default_factory=list)
    parent:object=None

    def cls(self,name):
        return name in self.attrs.get('class','').split()

    def ancestor(self,cls):
        el=self
        while el and not el.cls(cls):el=el.parent
        return el


class Page(HTMLParser):
    def __init__(self,source):
        super().__init__(convert_charrefs=False)
        self.src=source
        self.lines=[0]+[i+1 for i,c in enumerate(source) if c=='\n']
        self.byid={}
        self.nodes=[]
        self.stack=[]
        self.feed(source)

    def source_offset(self):
        row,col=self.getpos()
        return self.lines[row-1]+col

    def handle_starttag(self,tag,attrs):
        a=self.source_offset()
        b=a+len(self.get_starttag_text())
        node=Element(tag,dict(attrs),a,b,b,b)
        if self.stack:
            node.parent=self.stack[-1]
            node.parent.children.append(node)
        self.nodes.append(node)
        if 'id' in node.attrs:self.byid[node.attrs['id']]=node
        if tag not in VOID:self.stack.append(node)

    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.stack.pop()

    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].tag==tag:
                el=self.stack[i]
                el.close=self.source_offset()
                el.end=self.src.index('>',el.close)+1
                del self.stack[i:]
                return

    def raw(self,e):return self.src[e.start:e.end]
    def inside(self,e):return self.src[e.inner:e.close]


def patch(src,changes):
    # Equal-position inserts retain the order of their creation.
    last=len(src)
    for a,b,txt in reversed(sorted(changes,key=lambda x:(x[0],x[1]))):
        if b>last:raise ValueError(f'overlapping surgery at {a}/{b}/{last}')
        src=src[:a]+txt+src[b:]
        last=a
    return src


def alias(ids):
    return ''.join(f'<span class="lesson-anchor" id="{escape(x,quote=True)}"></span>' for x in dict.fromkeys(ids))


def ids(raw):
    return re.findall(r'\bid="([^"]+)"',raw)


def flatten(page,case_copy):
    edits=[]
    for e in page.nodes:
        if e.tag!='details' or not (e.cls('case-reference') or e.cls('provided-code')):continue
        summary=e.children[0]
        title=page.inside(summary)
        raw=page.raw(e)
        body=page.src[summary.end:e.close]
        key=e.attrs.get('id')
        if key in case_copy:
            new=case_copy[key]
            if new is None:
                edits.append((e.start,e.end,alias(ids(raw))))
                continue
            title,desc=map(escape,new)
            body=alias(i for i in ids(raw) if i!=key)+f'<p>{desc}</p>'
        nodeid=f' id="{key}"' if key else ''
        if e.cls('provided-code'):
            # The enclosing practice cell already introduces and labels this listing.
            out=body
        else:
            out=f'<div class="worked-case"{nodeid}><h3>{title}</h3>{body}</div>'
        edits.append((e.start,e.end,out))
    return Page(patch(page.src,edits))


def load_units():
    data={k:{} for k in ['PLACEMENTS','TOPIC_COPY','CASE_COPY','WORKFLOWS','INLINE_NOTES']}
    for f in sorted(Path(__file__).parent.glob('unit*.py')):
        mod=import_module(f.stem)
        for k,m in data.items():m.update(getattr(mod,k,{}))
    return data


def plain(raw):
    return unescape(re.sub('<[^>]*>','',raw)).strip()


def notebook_body(body):
    root=lh.fragment_fromstring(body,create_parent='div')
    for node in root.xpath('.//button | .//script | .//*[@aria-hidden="true"] | .//span[@class="code-actions"]'):
        node.drop_tree()
    for node in root.iter():
        for key in list(node.attrib):
            if key in ('id','class','tabindex','type','aria-label','style') or key.startswith('data-'):
                del node.attrib[key]
    for node in root.xpath('.//a[@href]'):
        if node.get('href','').startswith('#'):node.drop_tag()
    for node in list(root.xpath('.//span[not(normalize-space(.))]')):
        if node.getparent() is not None:node.drop_tree()
    for node in reversed(root.xpath('.//div | .//span')):node.drop_tag()
    return '\n\n'.join(lh.tostring(c,encoding='unicode',method='html').strip() for c in root).strip()


def transform(day,data,source,output,media):
    name=f'chapter{day:02}'
    old=source/name
    dest=output/name
    p=flatten(Page((old/'index.html').read_text()),data['CASE_COPY'].get(day,{}))
    nb=json.loads((old/(name+'.ipynb')).read_text())
    cells=nb['cells']
    positions={c['id']:i for i,c in enumerate(cells)}
    if day==116:
        for c in cells:
            if c['cell_type']=='markdown' and '98장의 수정 후 실행 결과 보기' in ''.join(c['source']):
                txt=''.join(c['source']).replace('<details><summary>98장의 수정 후 실행 결과 보기</summary>','### 98장의 수정 후 실행 결과').replace('</details>','')
                c['source']=(txt.rstrip()+'\n').splitlines(True)
    sections=[e for e in p.nodes if e.cls('lesson-section')]
    articles=[e for e in p.nodes if e.cls('notebook-cell')]
    bycell={int(e.attrs['data-cell']):e for e in articles}
    place=data['PLACEMENTS'].get(day,{})
    copy=data['TOPIC_COPY'].get(day,{})
    edits=[]
    inserts=defaultdict(list)
    nb_inserts=defaultdict(list)
    changed_titles=[]

    def target(anchor,media_first=False):
        if re.fullmatch(r'cell-\d+',anchor):el=bycell[int(anchor.split('-')[1])]
        else:el=p.byid.get(anchor)
        if el is None or (anchor=="sources" and not el.cls("lesson-section")):
            if anchor in ('sources','recap'):el=p.byid['recap']
            else:raise ValueError((day,anchor))
        art=el.ancestor('notebook-cell')
        if art:
            n=int(art.attrs['data-cell'])
            ix=positions[f'code-{n}']
            before=media_first and art.attrs.get('data-task')!='1'
            # Keep code, output, reflection, and folded practice solution together.
            return (art.start if before else art.end,ix-1 if before else positions.get(f'notes-{n}',ix)+1)
        sec=el.ancestor('lesson-section')
        if not sec:raise ValueError((day,anchor,'no section'))
        sid=sec.attrs['id']
        h=next(h for h in p.nodes if sec.start<h.start<sec.end and h.tag=='h2')
        subtitle=plain(p.inside(h))
        sec_pos=next((i for i,c in enumerate(cells) if c['cell_type']=='markdown' and (''.join(c['source']).splitlines() or [''])[0].strip()=='## '+subtitle),None)
        sec_pos=sec_pos if sec_pos is not None else (0 if sid=='start' else len(cells)-1)
        cell=next((e for e in articles if sec.inner<e.start<sec.close),None)
        if day==12 and sid=='langchain-parsers':
            return (next(e for e in sec.children if e.tag=='h3').start,sec_pos+1)
        return (cell.start if cell else sec.close,sec_pos+1)

    def insert(anchor,key,html,md='',attachments=None,is_media=False):
        off,idx=target(anchor,is_media)
        inserts[off].append(html)
        if md:
            entry={'cell_type':'markdown','id':key,'metadata':{},'source':(md.rstrip()+'\n').splitlines(True)}
            if attachments:entry['attachments']=attachments
            nb_inserts[idx].append(entry)

    read=p.byid.get('readings')
    visible_count=0
    if read:
        edits.append((read.start,read.end,''))
        topicids={ch.attrs.get('id') for ch in read.children if ch.cls('reading-topic')}
        if topicids!=set(place):raise ValueError((day,topicids^set(place)))
        aliases=['readings']
        for e in read.children:
            if e.tag=='span' and e.attrs.get('id'):
                aliases.append(e.attrs['id'])
            if not e.cls('reading-topic'):continue
            key=e.attrs['id']
            title=plain(p.inside(e.children[0]))
            content=p.src[e.children[0].end:e.close].strip()
            rawids=ids(content)
            replaced=key in copy
            cases=[c for c in p.nodes if c.cls('worked-case') and e.inner<c.start<e.close]
            saved_cases=''.join(p.raw(c) for c in cases if c.attrs.get('id') in data['CASE_COPY'].get(day,{}) or day==62)
            rawids=[i for i in rawids if i not in ids(saved_cases)]
            if replaced and copy[key] is None:
                insert(place[key],key,alias([*aliases,key,*rawids])+saved_cases,notebook_body(saved_cases) if saved_cases else '')
                aliases=[]
                continue
            if replaced:
                title,desc=copy[key]
                content='<p>'+escape(desc)+'</p>'+saved_cases
            intro=alias([*aliases,*(rawids if replaced else [])])
            group=f'{intro}<div class="lesson-explanation" id="{key}"><h3>{escape(title)}</h3>{content}</div>'
            insert(place[key],'inline-'+key,group,'### '+title+'\n\n'+notebook_body(content))
            changed_titles.append((title,key))
            visible_count+=1
            aliases=[]
        if aliases:raise ValueError((day,'unclaimed aliases',aliases))
        nav=next(e for e in p.nodes if e.tag=='nav' and e.attrs.get('aria-label')=='단원 목차')
        n=0
        for link in nav.children:
            if link.tag!='a':continue
            if link.attrs.get('href')=='#readings':
                edits.append((link.start,link.end,''));continue
            n+=1
            num=link.children[0]
            if p.inside(num)!=f'{n:02}':edits.append((num.inner,num.close,f'{n:02}'))
        for n,sec in enumerate([x for x in sections if x!=read],1):
            num=next(x for x in p.nodes if sec.inner<=x.start<sec.close and x.cls('section-number'))
            if p.inside(num)!=f'{n:02}':edits.append((num.inner,num.close,f'{n:02}'))

    for anchor,(title,desc) in data['INLINE_NOTES'].get(day,{}).items():
        key='note-'+anchor
        changed_titles.append((title,key))
        insert(anchor,key,f'<div class="lesson-explanation" id="{key}"><h3>{escape(title)}</h3><p>{escape(desc)}</p></div>',
               '### '+title+'\n\n'+desc)
    flows=data['WORKFLOWS'].get(day,[])
    media_anchors=set()
    for spec in flows:
        key='workflow-'+spec['slug']
        stem=media/name/key
        shutil.copyfile(stem.with_suffix('.mp4'),dest/(key+'.mp4'))
        gif=b64encode(stem.with_suffix('.gif').read_bytes()).decode()
        title,desc=spec['title'],spec['caption']
        title_html,desc_html=escape(title),escape(desc)
        rows=''.join('<li><strong>'+escape(dict(spec['nodes'])[k])+'</strong> · '+escape(str(field))+' = '+escape(str(value))+'</li>' for k,field,value,_ in spec['steps'])
        figure=(f'<figure class="lesson-clip workflow-clip" id="{key}"><h3>{title_html}</h3>'
                f'<video autoplay muted loop playsinline preload="metadata" src="{key}.mp4" aria-label="{title_html}" aria-describedby="{key}-caption"></video>'
                f'<figcaption id="{key}-caption">{desc_html}</figcaption><ol class="workflow-transcript" aria-label="실행 경로와 상태">{rows}</ol></figure>')
        location=target(spec['anchor'],True)[0]
        before=location not in media_anchors and not spec.get('after_code')
        media_anchors.add(location)
        insert(spec['anchor'],key,figure,f'### {title}\n\n![{title}](attachment:{key}.gif)\n\n{desc}',{key+'.gif':{'image/gif':gif}},before)
    edits.extend((off,off,'\n'+'\n'.join(contents)+'\n') for off,contents in inserts.items())
    page=patch(p.src,edits)
    if '심화 읽기' in page:
        # Occasional incidental references are deliberately reported for editorial review.
        print('review lingering link:',name,flush=True)
    (dest/'index.html').write_text(page)
    for index in sorted(nb_inserts,reverse=True):cells[index:index]=nb_inserts[index]
    (dest/(name+'.ipynb')).write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
    return dict(day=day,title=plain(p.inside(next(e for e in p.nodes if e.tag=='h1'))),topics=len(place),visible=visible_count,
                notes=changed_titles,flows=[(s['title'],'workflow-'+s['slug']) for s in flows])


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('previous_site',type=Path)
    ap.add_argument('media',type=Path)
    ap.add_argument('manifest',type=Path)
    ap.add_argument('--days',type=int,nargs='*')
    args=ap.parse_args()
    if args.previous_site.resolve()==(ROOT/'site').resolve():raise SystemExit('Use a separate source snapshot.')
    data=load_units()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(lambda i:transform(i,data,args.previous_site,ROOT/'site',args.media),args.days or range(1,117)))
    args.manifest.write_text(json.dumps(results,ensure_ascii=False,indent=2))
