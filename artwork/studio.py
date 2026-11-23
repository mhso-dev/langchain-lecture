"""Small drawing vocabulary for individually choreographed textbook illustrations.

Coordinates use a 640 × 218 board. Each chapter draws its own time-dependent
geometry. draw() is pure, so the same frames can be scrubbed on the web and
played in a kernel-free notebook attachment.
"""
from dataclasses import dataclass
from functools import lru_cache
import math
import os
from PIL import Image, ImageDraw, ImageFont
(W, H) = (640, 218)
SCALE = 1.25
INK = '#102438'
BLUE = '#1c58ac'
TEAL = '#087765'
RED = '#b64033'
GOLD = '#ab6518'
LIGHT = '#d8e5ef'
PAPER = '#ffffff'
MINT = '#c4eadb'
PINK = '#fbd9ce'
YELLOW = '#ffe8a9'
SKY = '#cce2fc'
MUTED = '#4d6473'
SCENES = {}

@dataclass
class Scene:
    chapter: int
    section: int
    key: str
    title: str
    explanation: str
    draw: object

def scene(chapter, section, key, title, explanation):

    def register(draw):
        if key in SCENES:
            raise ValueError(key)
        SCENES[key] = Scene(chapter, section, key, title, explanation, draw)
        return draw
    return register

def ease(t, start=0.1, end=0.84):
    f = min(1, max(0, (t - start) / (end - start)))
    return f * f * (3 - 2 * f)

def travel(t, a, b, start=0.1, end=0.84):
    return a + (b - a) * ease(t, start, end)

def step(t, values):
    return values[min(len(values) - 1, int(t * len(values)))]

@lru_cache(maxsize=160)
def font(size, bold):
    path = os.environ.get('LESSON_BOLD_FONT' if bold else 'LESSON_FONT', '/System/Library/Fonts/AppleSDGothicNeo.ttc')
    return ImageFont.truetype(path, round(size * SCALE), index=6 if bold and path.endswith('AppleSDGothicNeo.ttc') else 0)

class Board:

    def __init__(self, tint):
        self.image = Image.new('RGB', (round(W * SCALE), round(H * SCALE)), tint)
        self.pen = ImageDraw.Draw(self.image)

    def points(self, xy):
        return [round(v * SCALE) for v in xy]

    def rect(self, x, y, w, h, fill=PAPER, edge=None, r=5):
        if w <= 0 or h <= 0:
            return
        self.pen.rounded_rectangle(self.points((x, y, x + w, y + h)), radius=round(r * SCALE), fill=fill, outline=edge, width=2)

    def circ(self, x, y, r, fill=TEAL, edge=None):
        if r <= 0:
            return
        self.pen.ellipse(self.points((x - r, y - r, x + r, y + r)), fill=fill, outline=edge, width=2)

    def line(self, xy, color=INK, width=2):
        self.pen.line(self.points(xy), fill=color, width=max(1, round(width * SCALE)), joint='curve')

    def poly(self, xy, color):
        self.pen.polygon(self.points(xy), fill=color)

    def arc(self, x, y, r, a, b, color, width=4):
        self.pen.arc(self.points((x - r, y - r, x + r, y + r)), start=a, end=b, fill=color, width=round(width * SCALE))

    def text(self, x, y, s, size=19, color=INK, bold=False, maxw=None):
        s = str(s)
        while maxw and size > 11 and (self.pen.textlength(s, font=font(size, bold)) > maxw * SCALE):
            size -= 1
        self.pen.text(self.points((x, y)), s, font=font(size, bold), fill=color, anchor='mm', stroke_width=0)

    def chip(self, x, y, s, fill=SKY, w=112, h=40):
        self.rect(x - w / 2, y - h / 2, w, h, fill, INK, min(10, h / 2))
        self.text(x, y, s, 19, INK, True, w - 12)

    def page(self, x, y, w, h, title='', lines=3):
        self.rect(x + 4, y + 5, w, h, LIGHT, None, 3)
        self.rect(x, y, w, h, PAPER, INK, 3)
        self.poly((x + w - 16, y, x + w, y + 16, x + w - 16, y + 16), LIGHT)
        if title:
            self.text(x + w / 2, y + 19, title, 17, INK, True, w - 22)
        for i in range(lines):
            self.line((x + 12, y + 38 + i * 12, x + w - 15 - i % 2 * 15, y + 38 + i * 12), LIGHT, 3)

    def arrow(self, x, y, u, v, color=BLUE):
        self.line((x, y, u, v), color, 3)
        a = math.atan2(v - y, u - x)
        self.poly((u, v, u - 12 * math.cos(a - 0.46), v - 12 * math.sin(a - 0.46), u - 12 * math.cos(a + 0.46), v - 12 * math.sin(a + 0.46)), color)

    def lens(self, x, y, r=32):
        self.circ(x, y, r, None, BLUE)
        self.line((x + r * 0.68, y + r * 0.68, x + r * 1.4, y + r * 1.4), BLUE, 7)

    def meter(self, x, y, w, value, maxval, fill=TEAL):
        self.rect(x, y, w, 16, LIGHT, None, 7)
        self.rect(x, y, w * max(0, min(1, value / maxval)), 16, fill, None, 7)

    def cylinder(self, x, y, w, h, label):
        self.rect(x, y + 8, w, h, PAPER, INK, 8)
        self.pen.ellipse(self.points((x, y, x + w, y + 19)), fill=SKY, outline=INK, width=2)
        self.text(x + w / 2, y + h * 0.62, label, 19, INK, True, w - 12)

    def slot(self, x, y, w, s, fill=MINT):
        self.rect(x, y, w, 42, fill, INK, 3)
        self.line((x + 8, y + 7, x + w - 8, y + 7), PAPER, 2)
        self.text(x + w / 2, y + 24, s, 17, INK, True, w - 12)

    def dots(self, x, y, n, active, dx=26, fill=TEAL):
        for i in range(n):
            self.circ(x + dx * i, y, 8, fill if i < active else LIGHT, INK)

    def check(self, x, y, valid=True):
        if valid:
            self.line((x - 10, y, x - 3, y + 7, x + 11, y - 9), TEAL, 4)
        else:
            self.line((x - 8, y - 8, x + 8, y + 8), RED, 4)
            self.line((x - 8, y + 8, x + 8, y - 8), RED, 4)

    def ribbon(self, x, y, w, words, active=-1):
        cell = w / len(words)
        for (i, s) in enumerate(words):
            self.chip(x + (i + 0.5) * cell, y, s, YELLOW if active == i else PAPER, cell - 4, 38)

    def bracket(self, x1, x2, y, label, color=BLUE):
        self.line((x1, y - 7, x1, y, x2, y, x2, y - 7), color, 2)
        self.text((x1 + x2) / 2, y + 16, label, 16, color, True, max(60, x2 - x1 + 30))

    def lamp(self, x, y, on, r=11):
        self.circ(x, y, r, TEAL if on else LIGHT, INK)
        if on:
            for a in range(0, 360, 60):
                u = math.cos(math.radians(a))
                v = math.sin(math.radians(a))
                self.line((x + u * (r + 3), y + v * (r + 3), x + u * (r + 7), y + v * (r + 7)), TEAL, 2)

    def stamp(self, x, y, label, ok=True, w=106):
        color = TEAL if ok else RED
        self.rect(x - w / 2, y - 16, w, 32, MINT if ok else PINK, color, 3)
        self.text(x, y, label, 17, color, True, w - 8)
