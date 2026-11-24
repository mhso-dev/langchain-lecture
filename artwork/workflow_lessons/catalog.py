"""Build a directly linkable, chapter-by-chapter register from the integration manifest."""
import json
from html import escape
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
GROUPS=[(1,12,'Python과 LLM 기초'),(13,25,'LLM 워크플로와 RAG'),(26,34,'LangGraph와 검색 도구'),(35,52,'RAG 평가·화면·프로젝트'),(53,69,'SQL·에이전트·서비스'),(70,85,'저장·배포·웹 실습'),(86,100,'서비스 프로젝트 구현'),(101,116,'서비스 검증과 인계')]


def build(rows):
    page=['''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>장별 교재 개정 목록 · AI 엔지니어링 교재</title><link rel="stylesheet" href="../assets/catalog.css"><link rel="stylesheet" href="../assets/edition-list.css"></head>
<body><header><a href="../index.html">← 전체 교재</a><h1>장별 교재 개정 목록</h1>
<p>2026년 11월 24일 · 1~116장 웹 교재와 학생 노트북</p></header><main>''']
    scenes=sum(len(row['flows']) for row in rows)
    page.append(f'<p>각 장에서 새로 볼 수 있는 설명과 워크플로 영상 {scenes}편을 모았습니다. 제목을 누르면 해당 교재의 설명이나 장면으로 이동합니다.</p>')
    page.append('<nav class="edition-jumps" aria-label="장 범위">' + ''.join(f'<a href="#group-{lo}">{lo}~{hi}장</a>' for lo,hi,_ in GROUPS)+'</nav>')
    for lo,hi,heading in GROUPS:
        page.append(f'<section class="edition-group" id="group-{lo}"><h2>{lo}~{hi}장 · {heading}</h2><ul>')
        for row in rows[lo-1:hi]:
            n=row['day']
            base=f'../chapter{n:02}/index.html'
            title=escape(row['title'])
            page.append(f'<li id="chapter{n:02}"><h3><a href="{base}">{n}장 · {title}</a></h3>')
            if row['notes']:
                links=' · '.join(f'<a href="{base}#{key}">{escape(t)}</a>' for t,key in row['notes'][:2])
                extra=len(row['notes'])-2
                page.append('<p><strong>본문</strong> '+links+(f' 외 {extra}개' if extra>0 else '')+'</p>')
            if row['flows']:
                links=' · '.join(f'<a href="{base}#{key}">{escape(t)}</a>' for t,key in row['flows'])
                page.append('<p><strong>새 영상</strong> '+links+'</p>')
            page.append('</li>')
        page.append('</ul></section>')
    page.append('</main></body></html>')
    out=ROOT/'site/updates/index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text('\n'.join(page)+'\n')


if __name__=='__main__':
    build(json.loads(Path(sys.argv[1]).read_text()))
