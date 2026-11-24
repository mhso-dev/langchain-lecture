"""Render the new motion studies to silent inline MP4 and matching notebook GIFs."""
import argparse
from functools import lru_cache
from importlib import import_module
import os
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
from scenes import SCENES

W, H = 800, 380
FPS, SECONDS = 10, 8
PAPER, INK, SUB = '#f6f6ee', '#17342f', '#405d57'
TEAL, PALE, AMBER, LINE = '#007c72', '#d1eee2', '#f6cb71', '#bacbc2'
FONT = os.getenv('LESSON_FONT', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')


@lru_cache(maxsize=80)
def font(size):
    return ImageFont.truetype(FONT, size)


def text(draw, xy, value, size=23, color=INK, anchor='lm', width=None):
    if width:
        while size > 12 and draw.textlength(value, font=font(size)) > width:
            size -= 1
    draw.text(xy, value, fill=color, font=font(size), anchor=anchor)


def tile(draw, rect, fill, outline=None, radius=10):
    draw.rounded_rectangle(rect, radius, fill, outline, width=2)


def stretch(value):
    value = max(0, min(1, value))
    return value * value * (3 - 2 * value)


def correspond(draw, scene, pos):
    left, right, routes = scene['left'], scene['right'], scene['routes']
    k = min(int(pos * len(routes)), len(routes)-1)
    u = stretch((pos*len(routes)-k-.08)/.62)
    a, b = routes[k]
    def ys(items):
        return [218 + (j-(len(items)-1)/2)*64 for j in range(len(items))]
    ly, ry = ys(left), ys(right)
    text(draw, (36,104), scene['headings'][0], 20, SUB)
    text(draw, (490,104), scene['headings'][1], 20, SUB)
    for j,(l,r) in enumerate(routes):
        shade = TEAL if j==k else LINE
        draw.line((323,ly[l],476,ry[r]), fill=shade, width=4 if j==k else 2)
    for group, y, start, active, end, arrived in [(left,ly,26,a,323,True),(right,ry,476,b,774,u>.60)]:
        for j,name in enumerate(group):
            chosen=j==active and arrived
            tile(draw,(start,y[j]-23,end,y[j]+23),PALE if chosen else '#ffffff',TEAL if chosen else LINE)
            text(draw,((start+end)/2,y[j]),name,22,INK,'mm',end-start-20)
    x=323+(476-323)*u
    y=ly[a]+(ry[b]-ly[a])*u
    draw.ellipse((x-9,y-9,x+9,y+9),fill=AMBER,outline=INK,width=2)


def ledger(draw, scene, pos):
    snapshots, fields = scene['snapshots'], scene['fields']
    n=len(snapshots)
    k=min(int(pos*n),n-1)
    u=stretch((pos*n-k)/.46)
    labels, values=snapshots[k]
    previous=snapshots[max(0,k-1)][1]
    x0,x1=37,758
    for j,(label,_) in enumerate(snapshots):
        x=x0+(j+.5)*(x1-x0)/n
        if j: draw.line((x-(x1-x0)/n,100,x,100),fill=TEAL if j<=k else LINE,width=3)
    for j,(label,_) in enumerate(snapshots):
        x=x0+(j+.5)*(x1-x0)/n
        draw.ellipse((x-8,92,x+8,108),fill=AMBER if j==k else TEAL if j<k else PAPER,outline=INK,width=2)
        text(draw,(x,127),label,18,INK if j==k else SUB,'mm',(x1-x0)/n-8)
    for i,name in enumerate(fields):
        y=175+i*52
        tile(draw,(38,y-18,762,y+25),'#ffffff',LINE,7)
        text(draw,(54,y+4),name,20,SUB,width=256)
        draw.line((323,y-12,323,y+17),fill=LINE,width=2)
        changed=k==0 or previous[i]!=values[i]
        if changed:
            # A moving coloured underline identifies the exact cell being written.
            draw.rounded_rectangle((340,y+17,341+int(390*u),y+20),2,fill=TEAL)
        text(draw,(344,y+1),previous[i] if changed and u<.32 else values[i],23,TEAL if changed else INK,width=399)


def relay(draw, scene, pos):
    stops=scene['stops']
    n=len(stops)
    k=min(int(pos*n),n-1)
    progress=pos*n-k
    xs=[82+j*636/(n-1) for j in range(n)]
    for j,x in enumerate(xs):
        if j: draw.line((xs[j-1],155,x,155),fill=TEAL if j<=k else LINE,width=5)
    for j,(label,_,_) in enumerate(stops):
        x=xs[j]; r=15 if j==k else 11
        draw.ellipse((x-r,155-r,x+r,155+r),fill=AMBER if j==k else PALE,outline=TEAL,width=3)
        text(draw,(x,117),label,22,INK,'mm',155)
    u=stretch((progress-.42)/.5)
    x=xs[k]+(xs[min(k+1,n-1)]-xs[k])*u
    tile(draw,(x-10,145,x+10,165),AMBER,INK,4)
    _,var,value=stops[k]
    tile(draw,(46,207,754,309),'#173d37')
    text(draw,(70,235),var,20,'#99e3cb',width=655)
    text(draw,(70,276),value,28,'#ffffff',width=652)
    draw.line((x,178,x,203),fill=TEAL,width=2)


def cells(draw, xy, strings, highlight=-1):
    x,y=xy
    for j,name in enumerate(strings):
        tile(draw,(x,y+48*j,x+202,y+48*j+39),AMBER if j==highlight else '#ffffff',LINE)
        text(draw,(x+101,y+48*j+19),name,18,INK,'mm',188)


def handoff(draw, scene, pos):
    # Two values travel separately; the final writer receives both, not just billing.
    names=['summarize','classify','write']
    for j,(x,name) in enumerate(zip([42,306,570],names)):
        tile(draw,(x,91,x+178,129),INK)
        text(draw,(x+89,109),name,20,'#ffffff','mm')
    steps=[
        ('원래 문의','결제한 영수증을 어디에서 볼 수 있나요?'),
        ('summary','사용자가 결제 영수증 확인 방법을 문의했다.'),
        ('category','billing'),
        ('write가 받는 JSON','summary + category'),
    ]
    q=min(3,int(pos*4)); u=stretch((pos*4-q-.12)/.73)
    # The upper line carries summary past the classifier; the lower line carries its label.
    draw.line((130,141,130,167,660,167,660,139),fill=TEAL,width=4)
    draw.line((396,140,396,200,686,200,686,139),fill='#cf9230',width=4)
    def token(x,y,c):
        draw.ellipse((x-9,y-9,x+9,y+9),fill=c,outline=INK,width=2)
    if q==0: token(130,152,PALE)
    if q==1: token(130+266*u,167,PALE)
    if q==2: token(396,167,PALE);token(396,200,AMBER)
    if q==3: token(396+264*u,167,PALE);token(396+290*u,200,AMBER)
    tile(draw,(35,225,765,324),'#ffffff',LINE)
    text(draw,(55,248),steps[q][0],17,SUB)
    text(draw,(55,287),steps[q][1],28,INK,width=680)


def join_rows(draw, scene, pos):
    # Completed turns accumulate rather than showing the final counts ahead of time.
    groups=[0,0,1]; labels=['1 · alice','2 · alice','3 · bob']
    progress=min(3,pos*3.7); done=int(progress); local=stretch(progress-done)
    for i,name in enumerate(['학습자 A','학습자 B']):
        y=133+i*109
        tile(draw,(468,y-27,756,y+34),PALE,TEAL)
        text(draw,(484,y+3),name,22)
        count=sum(g==i for g in groups[:done])
        text(draw,(725,y+2),f'{count}건',27,TEAL,'rm')
    text(draw,(40,94),'course_turns',18,SUB)
    text(draw,(470,90),'GROUP BY   /   COUNT(*)',18,SUB)
    for i,owner in enumerate(groups):
        x,y=36,131+i*57
        if i<done:
            text(draw,(x,y),labels[i]+'  ✓',18,SUB); continue
        t=local if i==done else 0
        x+=(424-x)*t; y+=(133+109*owner-y)*t
        tile(draw,(x,y-20,x+154,y+20),AMBER if i==done else '#ffffff',LINE)
        text(draw,(x+77,y),labels[i],21,INK,'mm')


def shelves(draw, scene, pos, day):
    # Independent sheets make clearing one slot distinguishable from erasing its history.
    if day==29:
        left,right='thread A','thread B'
        phases=[('A에 첫 질문',['대출 기간?'],[]),('A에 이어서 질문',['대출 기간?','반납 방법?'],[]),
                ('B에서 새 대화',['대출 기간?','반납 방법?'],['첫 질문'])]
    else:
        left,right='질문 이력','현재 출처'
        phases=[('첫 질문을 기록',['대출 기간은?'],[]),('검색 결과를 표시',['대출 기간은?'],['library-1']),
                ('새 질문의 근거가 없음',['대출 기간은?','주차 요금은?'],[])]
    k=min(2,int(pos*3)); u=stretch((pos*3-k)/.55)
    text(draw,(35,95),phases[k][0],23)
    for j,title in enumerate([left,right]):
        x=39+j*377
        tile(draw,(x,147,x+340,307),'#e8eee9',LINE)
        tile(draw,(x,129,x+138,159),TEAL if not j else INK)
        text(draw,(x+69,143),title,19,'#ffffff','mm')
        values=phases[k][j+1]
        if not values: text(draw,(x+166,226),'[   ]',31,SUB,'mm')
        for i,value in enumerate(values):
            enter=not k or value not in phases[k-1][j+1]
            y=184+i*46-(1-u)*18*enter
            tile(draw,(x+17,y,x+322,y+36),AMBER if enter else '#ffffff',LINE)
            text(draw,(x+33,y+18),value,21)


def merge_candidates(draw, scene, pos):
    u=stretch((pos-.17)/.60)
    text(draw,(35,94),'질의별 적중',20,SUB)
    text(draw,(502,94),'ID 기준 후보 목록',20,SUB)
    for i,question in enumerate(['대출 기간은 며칠인가요?','대출 기간']):
        y=143+i*110
        text(draw,(35,y),question,22)
        x=42+452*u; yy=y+43+(208-y-43)*u
        tile(draw,(x,yy-18,x+229,yy+20),PALE if i==0 else '#ffdf99',TEAL)
        text(draw,(x+114,yy),'library-1:0',23,INK,'mm')
    if u>.93:
        text(draw,(610,275),'고유 청크  1건',24,TEAL,'mm')


def tx(draw,scene,pos):
    k=min(2,int(pos*3));u=stretch((pos*3-k)/.62)
    text(draw,(50,107),'현재 연결에서 읽은 값',21,SUB)
    text(draw,(478,107),'마지막 커밋',21,SUB)
    for x,name in [(46,'행 1'),(473,'행 1')]:
        for off in [10,5,0]: tile(draw,(x+off,143+off,x+265+off,270+off),'#e9eee8' if off else '#ffffff',LINE)
        text(draw,(x+17,163),name,17,SUB)
    text(draw,(602,219),'초안',29,INK,'mm')
    text(draw,(179,219),'수정한 초안' if k==1 or (k==2 and u<.55) else '초안',28,INK,'mm')
    if k==2:
        draw.line((457,217,333,217),fill=TEAL,width=4)
        x=447-103*u;draw.polygon([(x-10,217),(x+9,207),(x+9,227)],fill=TEAL)
    text(draw,(400,313),['조회','UPDATE · 현재 연결만 변경','rollback() · 확정된 값으로 복원'][k],21,TEAL,'mm')


def files(draw,scene,pos):
    k=min(2,int(pos*3))
    paths=['Skill 목록','evidence-answer/SKILL.md','references/source-check.md']
    for i,(name,x) in enumerate(zip(paths,[39,94,150])):
        y=112+i*74
        if i: draw.line((x-32,y-38,x-32,y,x-8,y),fill=TEAL,width=3)
        tile(draw,(x,y-20,x+540,y+30),PALE if i<=k else '#ecede7',TEAL if i==k else LINE)
        # File with a folded corner opens only when requested.
        draw.polygon([(x+13,y-10),(x+33,y-10),(x+42,y),(x+42,y+19),(x+13,y+19)],
                     fill=AMBER if i==k else '#ffffff',outline=INK)
        text(draw,(x+55,y+4),name,22,INK if i<=k else SUB)
        text(draw,(x+525,y+4),'읽음' if i<=k else '대기',17,TEAL if i<=k else SUB,'rm')
    text(draw,(42,314),'comparison-report 본문은 이 실행에서 열지 않습니다.',20,SUB)


def network(draw, scene, pos):
    text(draw,(35,96),'외부',21,SUB)
    tile(draw,(280,85,769,309),'#e2eee6',TEAL)
    text(draw,(300,104),'서비스 내부 네트워크',20,TEAL)
    nodes=[(86,204,'브라우저'),(365,204,'proxy'),(661,204,'api')]
    for i,(x,y,s) in enumerate(nodes):
        if i<2: draw.line((x+49,y,nodes[i+1][0]-48,y),fill=TEAL,width=4)
        tile(draw,(x-54,y-35,x+54,y+34),'#ffffff',INK)
        text(draw,(x,y),s,21,INK,'mm')
    text(draw,(217,165),'443',21,INK,'mm')
    text(draw,(514,165),'api:8000',21,INK,'mm')
    p=min(2.0,pos*2.55)
    k=min(1,int(p));u=stretch(p-k)
    x=nodes[k][0]+(nodes[k+1][0]-nodes[k][0])*u
    draw.ellipse((x-9,230,x+9,248),fill=AMBER,outline=INK,width=2)
    text(draw,(400,325),'HTTPS 요청이 프록시를 거쳐 API에 도착합니다.',19,SUB,'mm')


FOCUS = {13:handoff,29:lambda d,s,p:shelves(d,s,p,29),38:merge_candidates,
         41:lambda d,s,p:shelves(d,s,p,41),53:join_rows,54:tx,58:files,74:network}


def extra_scenes():
    items = {}
    for path in sorted(Path(__file__).parent.glob('extra_*.py')):
        items.update(import_module(path.stem).EXTRAS)
    return items


def frame(day, scene, index):
    pos=index/(FPS*SECONDS)
    im=Image.new('RGB',(W,H),PAPER)
    draw=ImageDraw.Draw(im)
    tile(draw,(0,0,W,67),INK,radius=0)
    text(draw,(24,34),scene['title'],29,'#ffffff',width=751)
    drawing = scene.get('paint') or FOCUS.get(day) or {'links':correspond,'ledger':ledger,'relay':relay}[scene['drawing']]
    drawing(draw,scene,pos)
    draw.line((26,348,774,348),fill=LINE,width=2)
    draw.line((26,348,27+int(747*pos),348),fill=TEAL,width=4)
    return im


def render(key, output):
    extra = str(key).startswith('extra-')
    day = int(str(key).split('-')[-1])
    scene = extra_scenes()[day] if extra else SCENES[day]
    stem = output / (('extra' if extra else 'chapter') + f'{day:02d}')
    fps=FPS
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-threads','1','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(stem.with_suffix('.mp4'))]
    frames=[]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for i in range(fps*SECONDS):
            im=frame(day,scene,i)
            proc.stdin.write(im.tobytes())
            if i%2==0:
                frames.append(im.resize((600,285),Image.Resampling.LANCZOS))
        proc.stdin.close()
        if proc.wait(): raise RuntimeError(f'ffmpeg failed for {day}')
    frames[0].save(stem.with_suffix('.gif'),save_all=True,append_images=frames[1:],duration=200,loop=0,optimize=True)


if __name__=='__main__':
    from concurrent.futures import ProcessPoolExecutor
    from functools import partial
    p=argparse.ArgumentParser()
    p.add_argument('out',type=Path)
    p.add_argument('days',nargs='*')
    p.add_argument('--workers',type=int,default=2)
    args=p.parse_args()
    args.out.mkdir(exist_ok=True,parents=True)
    with ProcessPoolExecutor(max_workers=args.workers) as workers:
        list(workers.map(partial(render,output=args.out),args.days or [*sorted(SCENES), *(f'extra-{n}' for n in sorted(extra_scenes()))]))
