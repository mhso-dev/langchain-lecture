import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, relative, basename, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from './vendor/marked/marked.mjs';

import {publishChapters, units} from './pre_mid_chapters.mjs';

const output = fileURLToPath(new URL('../dist/', import.meta.url));
const lessons = [
  ['diagnostic', '시작 진단'],
  ['python-basics', 'A · Python 문법'],
  ['python-patterns', 'B · Python 디자인 패턴'],
  ['team-git', '공통 · 팀 Git과 GitHub'],
  ['prompt-workshop', 'OpenAI SDK와 프롬프트 작성'],
  ['chat-workshop', '대화 이어 가기와 Streamlit 챗봇'],
];

const escape = (value) => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const joinText = (lines) => Array.isArray(lines) ? lines.join('') : lines ?? '';
const route = (slug) => slug + '/index.html';
function renderOutput(cellOutput) {
  if (cellOutput.output_type === 'error') {
    throw new Error('실행 오류가 저장된 셀: ' + cellOutput.ename);
  }
  const value = joinText(cellOutput.text ?? cellOutput.data?.['text/plain']);
  if (!value) return '';
  return `<div class="observed"><span>실행 결과</span><pre>${escape(value.replace(/\n$/, ''))}</pre></div>`;
}

function renderLesson(slug, label) {
  const folder = join(output, 'pre-mid', slug);
  const notebook = JSON.parse(readFileSync(join(folder, 'lesson.ipynb'), 'utf8'));
  const secondPart = ['prompt-workshop', 'chat-workshop'].includes(slug);
  const part = secondPart ? '2부 · OpenAI SDK와 챗봇' : '1부 · Python과 Git';
  const headings = [];
  let title;
  const body = notebook.cells.map((cell, index) => {
    const source = joinText(cell.source);
    if (cell.cell_type === 'code') {
      const block = `<pre><code>${escape(source)}</code></pre>`;
      const code = cell.metadata?.jupyter?.source_hidden
        ? `<details><summary>실행 환경 준비 코드 보기</summary>${block}</details>` : block;
      return `<div class="example">${code}${cell.outputs.map(renderOutput).join('')}</div>`;
    }
    if (cell.cell_type !== 'markdown') throw new Error(`${slug} 셀 ${index + 1}: 지원하지 않는 셀 형식`);
    // Answers already contain escaped code. Markdown would reinterpret blank lines inside <pre>.
    if (source.trim().startsWith('<details>') && source.trim().endsWith('</details>')) {
      return `<div class="reading">${source}</div>`;
    }
    let content = source;
    if (!title) {
      const firstHeading = /^# (.+)$/m.exec(content);
      if (firstHeading) {
        title = firstHeading[1].trim();
        content = content.replace(firstHeading[0], '');
      }
    }
    let headingNumber = 0;
    const html = marked.parse(content).replace(/href="([^":#?]+)\.md"/g, 'href="$1.html"').replace(/<h2>([\s\S]*?)<\/h2>/g, (_, heading) => {
      const id = `section-${cell.id ?? index}-${++headingNumber}`;
      headings.push(`<a href="#${escape(id)}">${heading}</a>`);
      return `<h2 id="${escape(id)}">${heading}</h2>`;
    });
    return `<div class="reading">${html}</div>`;
  }).join('\n');
  if (!title) throw new Error(slug + ' 노트북 첫 제목이 없습니다.');

  const materials = readdirSync(folder, {withFileTypes: true})
    .filter(entry => entry.isFile() && entry.name.endsWith('.md'))
    .map(entry => {
      const name = entry.name;
      const caption = ({'practice.md': '실습 활동지', 'cases.md': 'Git 사례 기록 양식', 'shift-records.md': '녹음실 교대 원장', 'change-requests.md': '야간 분실물 센터 변경 요청'})[name] ?? name;
      return `<a href="${encodeURIComponent(name.replace(/\.md$/, '.html'))}">${escape(caption)} 열기</a>`;
    }).join(' ');
  const navigation = lessons.map(([key, text]) => key === slug
    ? `<span aria-current="page">${text}</span>` : `<a href="../${route(key)}">${text}</a>`).join(' ');
  const following = {
    'team-git': ['../prompt-workshop/index.html', '다음 · 첫 모델 호출'],
    'prompt-workshop': ['../chat-workshop/index.html', '다음 · 대화 이어 가기'],
    'chat-workshop': ['../../chapter14/index.html', '다음 · 14장 첫 LCEL 체인'],
    'python-basics': ['../team-git/index.html', '다음 · 팀 Git과 GitHub'],
    'python-patterns': ['../team-git/index.html', '다음 · 팀 Git과 GitHub'],
  };
  const next = slug === 'diagnostic'
    ? `<a href="../${route('python-basics')}">A · Python 문법으로</a> <a href="../${route('python-patterns')}">B · 디자인 패턴으로</a>`
    : `<a href="${following[slug][0]}">${following[slug][1]}</a>`;
  const toc = headings.length > 1
    ? `<nav class="contents" aria-label="본문 차례">${headings.join(' ')}</nav>` : '';
  writeFileSync(join(folder, 'index.html'), `<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} · AI 엔지니어링 수업 교재</title>
<link rel="stylesheet" href="../../assets/reader.css"><link rel="stylesheet" href="../../assets/pre-mid.css"></head>
<body><a class="skip-link" href="#main">본문으로 건너뛰기</a>
<nav class="bookbar" aria-label="중간 프로젝트 전 교재"><a href="../../index.html">교재 홈</a>${navigation}</nav>
<main class="pre-mid" id="main"><header class="hero"><span class="chapter-tag">${part}</span><h1>${escape(title)}</h1>
<div class="materials"><a download href="lesson.ipynb">수업 노트북 받기</a> <a download href="../../daily/pre-mid.zip">1~42장 노트북과 실습 자료</a> ${materials}</div></header>
${toc}<article aria-label="${label} 본문">${body}</article>
<nav class="book-footer" aria-label="학습 순서">${next} <a href="#main">처음으로 ↑</a></nav></main></body></html>\n`);
}

for (const [slug, label] of lessons) renderLesson(slug, label);

function renderDocuments(directory) {
  for (const entry of readdirSync(directory, {withFileTypes: true})) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      renderDocuments(path);
      continue;
    }
    if (!entry.name.endsWith('.md')) continue;
    const source = readFileSync(path, 'utf8');
    const title = source.split('\n', 1)[0].replace(/^#\s+/, '');
    const prefix = relative(dirname(path), output).split('\\').join('/');
    const html = marked.parse(source).replace(/href="([^":#?]+)\.md"/g, 'href="$1.html"');
    writeFileSync(path.replace(/\.md$/, '.html'), `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)}</title>
<link rel="stylesheet" href="${prefix}/assets/reader.css"><link rel="stylesheet" href="${prefix}/assets/pre-mid.css"></head><body><a class="skip-link" href="#main">본문으로 건너뛰기</a>
<nav class="bookbar" aria-label="교재 이동"><a href="${prefix}/index.html#pre-mid-python">교재 홈</a><a download href="${encodeURIComponent(basename(path))}">원본 문서 받기</a></nav>
<main class="pre-mid" id="main"><article class="reading">${html}</article></main></body></html>\n`);
  }
}
renderDocuments(join(output, 'pre-mid'));

function insertAfterMain(file, block) {
  const page = readFileSync(file, 'utf8');
  if (!page.includes('<main>')) throw new Error('교재 연결 위치를 확인하세요: ' + file);
  writeFileSync(file, page.replace('<main>', '<main>' + block));
}
// Old bookmarks and notebook links follow the new teaching sequence on the static site.
const days = [
  ['diagnostic', '', '시작 진단과 Python 과정 선택'],
  ['python-basics', 'section-colors-01-1', '목록 복사와 정렬 기준', 'section-b11-1'],
  ['python-basics', 'section-filter-01-1', '조건 반복과 출력 형식', 'section-b19-1'],
  ['python-basics', 'section-calls-01-1', '함수와 포매터 연결', 'section-b28-1'],
  ['python-basics', 'section-counter-01-1', '독립적인 객체와 요구사항 변경', 'section-b42-1'],
  ['team-git', 'section-git-02-1', 'Git 브랜치와 워크트리'],
  ['team-git', 'section-git-20-1', 'GitHub PR과 동료 리뷰'],
  ['prompt-workshop', 'section-day08-1', 'LLM과 트랜스포머 이해하고 첫 요청 보내기'],
  ['prompt-workshop', 'section-day09-1', '독자와 목적에 맞게 프롬프트 고치기'],
  ['prompt-workshop', 'section-day10-1', '출력 예시와 빠진 정보 처리하기'],
  ['chat-workshop', 'section-day11-1', '대화 이력과 정정 요청'],
  ['chat-workshop', 'section-day12-1', 'Streamlit 채팅 화면과 세션 상태'],
  ['chat-workshop', 'section-day13-1', '후속 질문과 대화 초기화'],

];
const homePath = join(output, 'index.html');
const revised = [];
for (const [offset, [slug, anchor, title, patternAnchor]] of days.entries()) {
  const n = offset + 1;
  const chapter = 'chapter' + String(n).padStart(2, '0');
  const target = '../pre-mid/' + route(slug) + (anchor ? '#' + anchor : '');
  const folder = join(output, chapter);
  writeFileSync(join(folder, chapter + '.ipynb'), readFileSync(join(output, 'pre-mid', slug, 'lesson.ipynb')));
  writeFileSync(join(folder, 'index.html'), `<!doctype html><html lang="ko"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=${target}"><title>${title}</title><a href="${target}">${title}</a></html>`);
  revised.push({n, title, anchor, target, patternAnchor});
}
revised.push(...publishChapters(output));
const chapterPath = n => 'chapter' + String(n).padStart(2, '0') + '/index.html';
const sections = units.map(([first, last, label, hours], index) => {
  const cards = revised.slice(first-1,last).map(({n,title,patternAnchor}) => {
    const extra = patternAnchor ? `<a href="pre-mid/python-patterns/index.html#${patternAnchor}">B · 디자인 패턴 실습</a>` : '';
    return `<article class="card" data-search="${n}장 ${escape(label)} ${escape(title)}" data-available="true"><a href="${chapterPath(n)}"><span class="day">${n}장</span><h3>${escape(title)}</h3><span class="open">교재 읽기 →</span></a>${extra}</article>`;
  });
  return `<section class="unit" id="${index ? 'part-'+(index+1) : 'pre-mid-python'}"><h2>${index+1}부 · ${escape(label)} · ${hours}시간</h2><div class="grid">${cards.join('')}</div></section>`;
});
const catalog = readFileSync(homePath,'utf8');
const marker = '<!-- PRE_MID_CATALOG -->';
if (!catalog.includes(marker)) throw new Error('개편 목차 위치를 확인하세요.');
writeFileSync(homePath,catalog.replace(marker, () => '<p class="notice"><a href="pre-mid/course-guide.html">336시간 수업 운영표</a> · <a download href="daily/pre-mid.zip">1~42장 노트북과 실습 자료 받기</a></p>'+sections.join('\n')).replace('updates/index.html#classroom-edition','updates/index.html#pre-mid-336'));
const update = join(output, 'updates/index.html');
// Keep previous revision notes pointed at the source snapshot that they describe.
const archive = 'https://github.com/mhso-dev/langchain-lecture/blob/2ea3ce8dc28cf6d3e96c55a0d14cd8fbf27d034b/site/';
const history = readFileSync(update,'utf8').replace('이전 판에서 추가한 설명과 장면의 위치입니다. 개정한 절은 현재 본문에서 열립니다.', '이전 판의 기록입니다. 1~42장의 과거 항목은 당시 저장소 원본으로 연결됩니다.').replace(/href="\.\.\/(chapter(\d+)\/(?:index\.html|chapter\d+\.ipynb))(?:#[^"]*)?"/g,
  (original, path, n) => Number(n) <= 42 ? 'href="'+archive+path+'"' : original);
writeFileSync(update,history);
const changes = revised.map(({n,title,anchor,target}) => {
  const href = target ?? '../'+chapterPath(n)+'#'+anchor;
  return `<li><a href="${href}">${n}장 · ${escape(title)}</a></li>`;
});
insertAfterMain(update,`<section class="edition-group" id="pre-mid-336"><h2>11월 26일 · 중간 프로젝트 전 336시간 교재 개정</h2><p>1~42장의 본문, 실습 문제, 참고 답안과 자료를 여섯 부의 수업 순서에 맞췄습니다. 다음 목록은 각 장에서 새로 공부할 절로 연결됩니다.</p><ol>${changes.join('')}</ol><a download href="../daily/pre-mid.zip">1~42장 수업 묶음 받기</a></section>`);

insertAfterMain(update, `<section class="edition-group" id="model-settings"><h2>11월 26일 · 모델 설정과 캐시 실습</h2><ul>
<li><a href="../pre-mid/prompt-workshop/index.html#section-token-receipt-1">8장 · 첫 호출에서 입력·출력·합계 구분하기</a></li>
<li><a href="../chapter14/index.html#section-generation-settings-1">14장 · temperature와 출력 상한 비교하기</a> · <a href="../chapter14/index.html#section-answer-cache-1">LangChain 응답 캐시 실습</a></li>
<li><a href="../chapter24/index.html#section-cache-boundaries-1">24장 · 세 종류의 캐시와 캐시 읽기 토큰</a></li>
</ul></section>`);
