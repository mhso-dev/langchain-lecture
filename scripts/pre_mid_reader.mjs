import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, relative, basename, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from './vendor/marked/marked.mjs';

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
const links = (entries, prefix) => entries.map(([slug, label]) =>
  `<a href="${prefix}${route(slug)}">${label}</a>`).join(' ');

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
      const caption = ({'practice.md': '실습 활동지', 'cases.md': 'Git 사례 기록 양식'})[name] ?? name;
      return `<a href="${encodeURIComponent(name.replace(/\.md$/, '.html'))}">${escape(caption)} 열기</a>`;
    }).join(' ');
  const navigation = lessons.map(([key, text]) => key === slug
    ? `<span aria-current="page">${text}</span>` : `<a href="../${route(key)}">${text}</a>`).join(' ');
  const following = {
    'team-git': ['../prompt-workshop/index.html', '다음 · 첫 모델 호출'],
    'prompt-workshop': ['../chat-workshop/index.html', '다음 · 대화 이어 가기'],
    'chat-workshop': ['../../chapter14/index.html', '다음 · 분류 함수와 조건부 라우팅'],
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
<div class="materials"><a download href="lesson.ipynb">수업 노트북 받기</a> ${materials}</div></header>
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

function documentLinks(prefix) {
  return `<p>후속 단원 실습 자료</p><nav aria-label="실습 자료"><a href="${prefix}documents/questions/club-workshop.html">동아리 공지</a> <a href="${prefix}documents/questions/loan-inquiries.html">대여 문의와 답변 검토</a> <a href="${prefix}documents/recorder-practice.html">녹음기 설명서와 평가 질문</a></nav>`;
}

function insertAfterMain(file, block) {
  const page = readFileSync(file, 'utf8');
  if (!page.includes('<main>')) throw new Error('교재 연결 위치를 확인하세요: ' + file);
  writeFileSync(file, page.replace('<main>', '<main>' + block));
}
insertAfterMain(join(output, 'index.html'), `<section class="pre-mid-entry" id="pre-mid-python"><h2>중간 프로젝트 전 교재 · 1부 Python과 Git</h2>
<p>처음에는 진단을 풀고 A와 B 중 한 과정을 선택하세요. 두 과정 모두 팀 Git 실습으로 이어집니다.</p><nav aria-label="개편 교재 바로가기">${links(lessons.slice(0, 4), 'pre-mid/')}</nav><h2>2부 · OpenAI SDK와 프롬프트, 대화형 챗봇</h2><nav aria-label="2부 교재">${links(lessons.slice(4), 'pre-mid/')}</nav>${documentLinks('pre-mid/')}</section>`);
insertAfterMain(join(output, 'updates/index.html'), `<section id="pre-mid-python"><h2>11월 26일 · 1~13일 Python·Git과 OpenAI SDK 교재</h2>
<p>진단, Python 선택 과정 두 가지, 팀 Git 실습, 프롬프트 작성과 대화형 챗봇 수업을 새로 썼습니다. 각 교재에서 노트북을 내려받고 문제 아래에서 풀이를 열 수 있습니다.</p><nav aria-label="개정 교재">${links(lessons, '../pre-mid/')}</nav>${documentLinks('../pre-mid/')}</section>`);

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
let catalog = readFileSync(homePath, 'utf8');
for (const [offset, [slug, anchor, title, patternAnchor]] of days.entries()) {
  const day = offset + 1;
  const chapter = 'chapter' + String(day).padStart(2, '0');
  const target = '../pre-mid/' + route(slug) + (anchor ? '#' + anchor : '');
  const folder = join(output, chapter);
  writeFileSync(join(folder, chapter + '.ipynb'), readFileSync(join(output, 'pre-mid', slug, 'lesson.ipynb')));
  writeFileSync(join(folder, 'index.html'), `<!doctype html><html lang="ko"><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=${target}"><title>${title}</title><a href="${target}">${title}</a></html>`);
  const match = new RegExp('<article class="card"[^>]*><a href="' + chapter + '/index\\.html">[\\s\\S]*?</article>');
  if (!match.test(catalog)) throw new Error(chapter + ' 기존 목차를 찾을 수 없습니다.');
  const extra = patternAnchor ? `<a href="pre-mid/python-patterns/index.html#${patternAnchor}">B · 디자인 패턴 실습</a>` : '';
  catalog = catalog.replace(match, `<article class="card" data-search="${day}일차 ${title} ${day <= 7 ? "Python Git" : "OpenAI SDK 프롬프트 챗봇"}" data-available="true"><a href="${chapter}/index.html"><h3>${title}</h3><span class="open">${patternAnchor ? 'A · 문법 실습' : '교재 읽기'} →</span></a>${extra}</article>`);
}
catalog = catalog.replace('<h2>Python·개발 환경</h2>', '<h2>Python과 팀 Git</h2>')
  .replace('<h2>서비스·SDK·도구 루프</h2>', '<h2>OpenAI SDK와 프롬프트·챗봇</h2>')
  .replace(/<article class="card"[^>]*><a href="chapter14\/index\.html">/,
    '</div></section><section class="unit"><h2>SDK와 도구 루프</h2><div class="grid">$&');
writeFileSync(homePath, catalog);
