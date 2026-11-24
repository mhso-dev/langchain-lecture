"""Render each worked execution path as a silent MP4 and a matching notebook GIF."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache, partial
from importlib import import_module
from itertools import permutations
import math
import os
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 840, 490, 8
BG, INK, DIM = '#f4f6f2', '#153b38', '#425f5d'
TEAL, ORANGE, RAIL = '#006b63', '#ffcb79', '#8fa7a3'
FONT = os.environ.get('LESSON_FONT', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')


@lru_cache(None)
def font(size):
    return ImageFont.truetype(FONT, size)


def lettering(draw, xy, s, size, width, fill, anchor='lm'):
    while size > 12 and font(size).getlength(s) > width:
        size -= 1
    draw.text(xy, s, fill=fill, font=font(size), anchor=anchor)


def wrap(s, size, width):
    lines = ['']
    for token in str(s).split(' '):
        current = (lines[-1]+' '+token).strip()
        if lines[-1] and font(size).getlength(current) > width:
            lines.append(token)
        else:
            lines[-1] = current
    return lines


def delta(u, v):
    return (v[0]-u[0], v[1]-u[1])


def orientation(a,b,c):
    x,y=delta(a,b)
    X,Y=delta(a,c)
    return x*Y-y*X


def distance_to_segment(p,a,b):
    x,y=delta(a,b)
    t=max(0,min(1,((p[0]-a[0])*x+(p[1]-a[1])*y)/(x*x+y*y)))
    return math.dist(p,(a[0]+t*x,a[1]+t*y))


def layout(keys, edges):
    n=len(keys)
    if n<=3:
        slots=[(W*(i+.5)/n,159) for i in range(n)]
    else:
        upper=(n+1)//2
        slots=[(W*(i+.5)/upper,107) for i in range(upper)]
        slots+= [(W*(i+.5)/(n-upper),228) for i in reversed(range(n-upper))]
    routes=[(keys.index(a),keys.index(b)) for a,b in edges if a!=b]
    def score(pos):
        total=0
        for i,j in routes:
            a,b=pos[i],pos[j]
            total+=math.dist(a,b)*.06
            for k,p in enumerate(pos):
                if k!=i and k!=j and distance_to_segment(p,a,b)<74:
                    total+=600
        for k,(i,j) in enumerate(routes):
            for m,n in routes[k+1:]:
                if len({i,j,m,n})<4:continue
                a,b,c,d=pos[i],pos[j],pos[m],pos[n]
                if orientation(a,b,c)*orientation(a,b,d)<0 and orientation(c,d,a)*orientation(c,d,b)<0:
                    total+=380
        total+= math.dist(pos[0],slots[0])*.19
        total+= sum(math.dist(p,s)*.012 for p,s in zip(pos,slots))
        return total
    if n>7:raise ValueError(f'Too many nodes: {keys}')
    best=min(permutations(slots),key=score)
    return dict(zip(keys,best))


def route(a,b,bidirectional,half):
    if a==b:
        x,y=a
        return [(x+half*.4,y-25),(x+half*.4,y-44),(x-half*.4,y-44),(x-half*.4,y-25)]
    dx,dy=delta(a,b)
    length=math.hypot(dx,dy)
    ux,uy=dx/length,dy/length
    offset=11 if bidirectional else 0
    scale=min((half+3)/max(abs(ux),.001),29/max(abs(uy),.001))
    return [(a[0]+scale*ux-offset*uy,a[1]+scale*uy+offset*ux),
            (b[0]-scale*ux-offset*uy,b[1]-scale*uy+offset*ux)]


def on_path(points,t):
    ds=[math.dist(a,b) for a,b in zip(points,points[1:])]
    remaining=t*sum(ds)
    for a,b,d in zip(points,points[1:],ds):
        if remaining<=d and d:return (a[0]+(b[0]-a[0])*remaining/d,a[1]+(b[1]-a[1])*remaining/d)
        remaining-=d
    return points[-1]


def arrow(draw,points,color,width):
    draw.line(points,fill=color,width=width)
    (x,y),(u,v)=points[-2:]
    angle=math.atan2(v-y,u-x)
    draw.polygon([(u,v),*((u-11*math.cos(angle+s),v-11*math.sin(angle+s)) for s in [-.46,.46])],fill=color)


def background(day,s):
    im=Image.new('RGB',(W,H),BG)
    d=ImageDraw.Draw(im)
    lettering(d,(26,31),s['title'],30,765,INK)
    d.line((25,59,W-25,59),fill='#d3ded9',width=2)
    d.rounded_rectangle((18,279,W-18,H-18),16,fill='#173c39')
    return im


def frame(base, spec, pos, paths, tick, ticks):
    im=base.copy()
    d=ImageDraw.Draw(im)
    steps=spec['steps']
    ix=min(int(tick*len(steps)/ticks),len(steps)-1)
    frac=(tick*len(steps)/ticks)-ix
    key,field,value,note=steps[ix]
    played=[(x[0],y[0]) for x,y in zip(steps[:ix],steps[1:ix+1])]
    active=played[-1] if played else None
    for edge,points in paths.items():
        arrow(d,points,TEAL if edge in played else RAIL,4 if edge in played else 2)
    if active in paths:
        x,y=on_path(paths[active],min(1,frac/.53))
        d.ellipse((x-7,y-7,x+7,y+7),fill=ORANGE,outline=INK,width=2)
    half=78 if len(pos)>5 else 91
    for node,label in spec['nodes']:
        x,y=pos[node]
        hit=node==key
        done=node in [s[0] for s in steps[:ix]]
        d.rounded_rectangle((x-half,y-24,x+half,y+24),11,fill=TEAL if hit else '#e4eee9' if done else '#ffffff',outline=INK if hit else '#73948c',width=3 if hit else 2)
        lettering(d,(x,y),label,23,2*half-13,'white' if hit else INK,'mm')
    name=dict(spec['nodes'])[key]
    lettering(d,(38,308),name+'   /   '+str(field),22,665,'#bde5d8')
    lettering(d,(W-36,308),f'{ix+1} / {len(steps)}',21,85,'#c8ded7','rm')
    val_lines=wrap(str(value),29,W-85)
    for k,ln in enumerate(val_lines if len(val_lines)<=2 else [str(value)]):
        lettering(d,(38,352+30*k),ln,31,W-76,'#ffffff')
    desc=wrap(str(note),22,W-83)
    for k,line in enumerate(desc if len(desc)<=2 else [str(note)]):
        lettering(d,(38,417+26*k),line,22,W-78,'#dcece5')
    return im


def render(item, output):
    day,spec=item
    name=f'chapter{day:02}/workflow-'+spec['slug']
    path=output/name
    path.parent.mkdir(parents=True,exist_ok=True)
    keys=[x[0] for x in spec['nodes']]
    edges=[tuple(e) for e in spec['edges']]
    steps=spec['steps']
    for a,b in zip(steps,steps[1:]):
        if a[0]!=b[0] and (a[0],b[0]) not in edges:raise ValueError((name,a,b))
    pos=layout(keys,edges)
    paths={e:route(pos[e[0]],pos[e[1]],e[::-1] in edges,78 if len(pos)>5 else 91) for e in edges}
    base=background(day,spec)
    ticks=min(10,max(7,len(steps)*2))*FPS
    cmd=[os.environ.get('FFMPEG','ffmpeg'),'-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-threads','1','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(path.with_suffix('.mp4'))]
    gif=[]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for i in range(ticks):
            im=frame(base,spec,pos,paths,i,ticks)
            proc.stdin.write(im.tobytes())
            if i%2==0:gif.append(im.resize((588,343),Image.Resampling.LANCZOS))
        proc.stdin.close()
        if proc.wait():raise RuntimeError(name)
    gif[0].save(path.with_suffix('.gif'),save_all=True,append_images=gif[1:],duration=250,loop=0)
    return name


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--days',type=int,nargs='*')
    ap.add_argument('--workers',type=int,default=4)
    args=ap.parse_args()
    items=[(d,s) for f in sorted(Path(__file__).parent.glob('unit*.py')) for d,specs in getattr(import_module(f.stem),'WORKFLOWS',{}).items() for s in specs if not args.days or d in args.days]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for name in pool.map(partial(render,output=args.output),items): print(name,flush=True)
