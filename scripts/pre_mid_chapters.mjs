import {readFileSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {marked} from './vendor/marked/marked.mjs';

export const units = [
  [1, 7, 'Python과 팀 Git', 56],
  [8, 13, 'OpenAI SDK로 글을 쓰고 챗봇 만들기', 48],
  [14, 24, 'LCEL로 근거를 찾는 문서 챗봇 만들기', 88],
  [25, 32, 'OpenAI SDK로 문의 검토 워크플로 만들기', 64],
  [33, 39, 'LangGraph로 답변·재검색·보류 연결하기', 56],
  [40, 42, 'LangSmith로 설명서 챗봇 평가하기', 24],
];
const escape = text => text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const joinText = value => Array.isArray(value) ? value.join('') : value || '';
const chapter = n => 'chapter'+String(n).padStart(2, '0');

function markdown(text) {
  // In the downloaded pack the notebook sits beside pre-mid/. On the web it has a chapter folder.
  return marked.parse(text).replace(/href="(?:\.\/)?pre-mid\//g, 'href="../pre-mid/')
    .replace(/href="(\.\.\/pre-mid\/[^"?#]+)\.md(?=[#"])/g, 'href="$1.html')
    .replace(/<details(?:\s+open)?>/g, '<details class="notebook-answer">');
}

export function publishChapters(out) {
  const published = [];
  for (let n = 14; n <= 42; n++) {
    const dir = join(out, chapter(n));
    const file = chapter(n)+'.ipynb';
    const book = JSON.parse(readFileSync(join(dir,file), 'utf8'));
    const contents = [];
    let title;
    let firstHeading;
    const body = book.cells.map((cell, index) => {
      let text = joinText(cell.source);
      if (cell.cell_type === 'code') {
        const outputs = (cell.outputs ?? []).map(o => {
          if (o.output_type === 'error') throw new Error(file + ': ' + o.ename);
          const value = joinText(o.text ?? o.data?.['text/plain']);
          return value ? '<div class="observed"><span>실행 결과</span><pre>'+escape(value.trimEnd())+'</pre></div>' : '';
        }).join('');
        return '<div class="example"><pre><code>'+escape(text)+'</code></pre>'+outputs+'</div>';
      }
      if (index === 0) {
        const header = /^#\s+(.+)$/m.exec(text);
        if (!header) throw new Error(file + ': 장 제목 누락');
        title = header[1].trim();
        text = text.replace(header[0], '');
      }
      const blocks = text.split(/(^```mermaid\n[\s\S]*?\n```\s*$)/gm);
      let headingNo = 0;
      return blocks.map(block => {
        if (block.startsWith('```mermaid\n')) {
          const diagram = block.trimEnd().slice('```mermaid\n'.length,-4);
          if (/<\/script/i.test(diagram)) throw new Error(file + ': 흐름도 레이블을 확인하세요');
          return '<figure class="workflow-reading" data-workflow><h3>실행 경로</h3><div class="workflow-view" hidden></div><script type="text/plain">'+diagram+'</script></figure>';
        }
        const html = markdown(block).replace(/<h2>([\s\S]*?)<\/h2>/g, (_, label) => {
          const id = 'section-'+cell.id+'-'+(++headingNo);
          firstHeading ??= id;
          contents.push('<a href="#'+id+'">'+label+'</a>');
          return '<h2 id="'+id+'">'+label+'</h2>';
        });
        return '<div class="reading">'+html+'</div>';
      }).join('');
    }).join('\n');
    if (!firstHeading) throw new Error(file + ': 장별 소제목 누락');
    const unit = units.find(([first,last]) => first <= n && n <= last);
    const scripts = body.includes('data-workflow') ? '<link rel="stylesheet" href="../assets/guided-reading.css"><script defer src="../assets/mermaid/mermaid.tiny.js"></script><script defer src="../assets/workflows.js"></script>' : '';
    const unitMaterials = {
      14: ['rag/investigations', '설명서 검색 실습지'],
      25: ['workflow/workshop', '대여 문의 담당자 실습 기록지'],
      33: ['graph/workshop', '그래프 실습 수첩'],
      40: ['evaluation/fieldbook', '챗봇 품질 검토 활동지'],
    };
    const [material, caption] = unitMaterials[unit[0]];
    const worksheet = `<a href="../pre-mid/documents/${material}.html">${caption}</a>`;
    const transfer = n === 24 ? '<a href="../pre-mid/documents/transfer/handbook-lab.html">새 문서로 실습 · 36쪽 운영 편람</a>' : '';
    const nav = '<a href="../'+chapter(n-1)+'/index.html">이전 · '+(n-1)+'장</a> <a href="../'+chapter(n+1)+'/index.html">다음 · '+(n+1)+'장</a>';
    const page = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)}</title><link rel="stylesheet" href="../assets/reader.css"><link rel="stylesheet" href="../assets/pre-mid.css">${scripts}</head>
<body><a class="skip-link" href="#main">본문으로 건너뛰기</a><nav class="bookbar" aria-label="교재 이동"><a href="../index.html">전체 목차</a>${nav}</nav>
<main class="pre-mid" id="main"><header class="hero"><span class="chapter-tag">${escape(unit[2])}</span><h1>${escape(title)}</h1><div class="materials"><a download href="${file}">이 장의 노트북</a><a download href="../daily/pre-mid.zip">1~42장 노트북과 실습 자료</a>${worksheet}${transfer}</div></header>
<nav class="contents" aria-label="이 장의 차례">${contents.join(' ')}</nav><article id="guided-reading">${body}</article><nav class="book-footer" aria-label="학습 순서">${nav}<a href="#main">처음으로 ↑</a></nav></main></body></html>`;
    writeFileSync(join(dir, 'index.html'), page);
    published.push({n, title:title.replace(/^\d+장\s*[·.:-]?\s*/, ''), anchor:firstHeading});
  }
  return published;
}
