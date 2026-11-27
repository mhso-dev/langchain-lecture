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
    return `<div class="reading" id="cell-${escape(cell.id ?? String(index))}">${html}</div>`;
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
    let html = marked.parse(source).replace(/href="([^":#?]+)\.md"/g, 'href="$1.html"');
    if (path === join(output, 'pre-mid', 'reading-guide.md')) {
      // Keep notebook links usable in the offline guide and open the same cells in the web reader.
      html = html.replace(/href="([^"]+)\/lesson\.ipynb/g, 'href="$1/index.html')
        .replace(/href="\.\.\/(chapter\d+)\.ipynb/g, 'href="../$1/index.html')
        .replaceAll('#cell-id=', '#cell-');
      html += '<p><a download href="../daily/pre-mid.zip">전반부 실습 노트북과 자료 받기</a></p>';
    }
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
writeFileSync(homePath,catalog.replace(marker, () => '<p class="notice"><a href="pre-mid/reading-guide.html">전반부 1~42장 개정 교재</a> · <a href="pre-mid/course-guide.html">336시간 수업 운영표</a> · <a download href="daily/pre-mid.zip">1~42장 노트북과 실습 자료 받기</a></p>'+sections.join('\n')).replace('updates/index.html#classroom-edition','updates/index.html#cumulative-practice'));
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


insertAfterMain(update, `<section class="edition-group" id="function-reading"><h2>11월 27일 · 함수와 명령어로 읽는 전반부 교재</h2><p>함수의 역할을 읽고 짧은 호출 예제에서 입력과 결과를 확인한 뒤 응용 실습으로 넘어갑니다. 14장에서는 번역할 단어 하나로 프롬프트를 만들고 모델에 보낼 문장을 직접 출력합니다. 1~5장의 디자인 패턴 선택 과정은 <a href="../pre-mid/python-patterns/index.html">Python 디자인 패턴</a>에서 엽니다.</p><ol>${changes.join('')}</ol></section>`);

insertAfterMain(update, `<section class="edition-group" id="whole-reading"><h2>11월 27일 · 전반부 1~42장 본문과 실습 개정</h2><p>각 링크는 바뀐 설명이나 실습으로 연결됩니다. 1~5장은 문법 과정입니다. 디자인 패턴 과정에서는 <a href="../pre-mid/python-patterns/index.html#cell-rule-tie-goal">정렬 기준 실습</a>부터 읽을 수 있습니다.</p><ol>
<li><a href="../pre-mid/python-basics/index.html#cell-a1-shift-01">1장 · //와 %로 몫과 나머지 구하기</a></li>
<li><a href="../pre-mid/python-basics/index.html#cell-a2-shift-01">2장 · 리스트 위치와 딕셔너리 키로 값 하나 읽기</a></li>
<li><a href="../pre-mid/python-basics/index.html#cell-a3-shift-01">3장 · len과 sum으로 개수와 합 구하기</a></li>
<li><a href="../pre-mid/python-basics/index.html#cell-a4-shift-01">4장 · raise ValueError로 인자의 범위 검사하기</a></li>
<li><a href="../pre-mid/python-basics/index.html#cell-a5-shift-01">5장 · 클래스 속성과 인스턴스 속성 구분하기</a></li>
<li><a href="../pre-mid/team-git/index.html#cell-git-08">6장 · git worktree add로 두 번째 작업 폴더 열기</a></li>
<li><a href="../pre-mid/team-git/index.html#cell-git-sync-01">7장 · git fetch로 origin/main 갱신하고 로컬 main과 비교하기</a></li>
<li><a href="../pre-mid/prompt-workshop/index.html#cell-prompt-5">8장 · responses.create의 instructions와 input 나누기</a></li>
<li><a href="../pre-mid/prompt-workshop/index.html#cell-prompt-14">9장 · ask에서 입력을 고정하고 지시문만 바꾸기</a></li>
<li><a href="../pre-mid/prompt-workshop/index.html#cell-typed-output-heading">10장 · 문자열과 None을 받는 필드 선언하기</a></li>
<li><a href="../pre-mid/chat-workshop/index.html#cell-inspect-what-sent">11장 · 목록 슬라이스로 직전 요청에 포함된 메시지 읽기</a></li>
<li><a href="../pre-mid/chat-workshop/index.html#cell-echo-first">12장 · st.chat_input과 session_state로 입력한 문장 다시 그리기</a></li>
<li><a href="../pre-mid/chat-workshop/index.html#cell-exercise13">13장 · 새 대화 버튼 완성하기</a></li>
<li><a href="../chapter14/index.html#cell-parser-local-heading">14장 · StrOutputParser에 짧은 응답 메시지 넣기</a></li>
<li><a href="../chapter15/index.html#cell-page-id-check-goal">15장 · PDF 둘째 쪽을 다시 찾을 값 출력하기</a></li>
<li><a href="../chapter16/index.html#cell-chunk-source-goal">16장 · 길이를 바꿔도 출처가 남을까요?</a></li>
<li><a href="../chapter17/index.html#cell-rag-17-case-why">17장 · Chroma의 upsert와 query로 문단 저장하고 검색하기</a></li>
<li><a href="../chapter18/index.html#cell-rag-18-03">18장 · open_index의 반환값으로 저장된 컬렉션 다시 읽기</a></li>
<li><a href="../chapter19/index.html#cell-join-context-heading">19장 · join으로 ID와 본문을 함께 전달하기</a></li>
<li><a href="../chapter20/index.html#cell-date-edge-goal">20장 · 마지막 날도 유효한지 확인하기</a></li>
<li><a href="../chapter21/index.html#cell-rag-21-07">21장 · answer_from_documents의 답을 제공한 근거와 대조하기</a></li>
<li><a href="../chapter22/index.html#cell-rank-cut-goal">22장 · k만 바꾸어 누락된 정답 찾기</a></li>
<li><a href="../chapter23/index.html#cell-rag-23-case-why">23장 · 답만 읽을 때 가려지는 검색 실패</a></li>
<li><a href="../chapter24/index.html#cell-rag-24-06">24장 · cache_data와 cache_resource를 적용한 PDF 앱 만들기</a></li>
<li><a href="../chapter25/index.html#cell-w25-15">25장 · 중간 변수만 바꿔 답이 어긋난 단계 찾기</a></li>
<li><a href="../chapter26/index.html#cell-label-bound-goal">26장 · 낯선 라벨을 처리 함수 앞에서 걸러내기</a></li>
<li><a href="../chapter27/index.html#cell-w27-10">27장 · 두 번째 ask에도 원래 draft 전달하기</a></li>
<li><a href="../chapter28/index.html#cell-resume-failed-heading">28장 · 재시도 결과로 실패한 항목만 교체하기</a></li>
<li><a href="../chapter29/index.html#cell-json-two-errors-heading">29장 · JSON으로 읽어도 작업 목록인지 따로 검사하기</a></li>
<li><a href="../chapter30/index.html#cell-w30-14">30장 · revision_input에 초안과 feedback을 함께 넣기</a></li>
<li><a href="../chapter31/index.html#cell-zero-rewrite-goal">31장 · 수정 한도가 0이면 평가는 몇 번 일어날까요?</a></li>
<li><a href="../chapter32/index.html#cell-w32-06">32장 · run_step에서 한 번의 호출을 기록하고 process로 묶기</a></li>
<li><a href="../chapter33/index.html#cell-graph-33-10">33장 · stream_mode=&quot;updates&quot;로 노드의 반환값 하나씩 읽기</a></li>
<li><a href="../chapter34/index.html#cell-graph-34-05">34장 · add_conditional_edges의 출발 노드와 분기 함수 연결하기</a></li>
<li><a href="../chapter35/index.html#cell-graph-35-04">35장 · InMemorySaver와 thread_id로 대화 이어 가기</a></li>
<li><a href="../chapter36/index.html#cell-graph-36-07">36장 · 고정한 문단 하나로 connect의 노드 연결 확인하기</a></li>
<li><a href="../chapter37/index.html#cell-quote-id-goal">37장 · 인용문이 같아도 ID가 틀리면 어떻게 될까요?</a></li>
<li><a href="../chapter38/index.html#cell-route-state-goal">38장 · 두 번째 검색에서 근거를 찾으면 어디로 갈까요?</a></li>
<li><a href="../chapter39/index.html#cell-graph-39-05">39장 · st.session_state에 실행 결과를 저장하고 다시 표시하기</a></li>
<li><a href="../chapter40/index.html#cell-ls40-12">40장 · examples로 평가 입력과 참고 답을 따로 읽기</a></li>
<li><a href="../chapter41/index.html#cell-eligible-score-goal">41장 · 보류가 정답이면 무엇을 채점할까요?</a></li>
<li><a href="../chapter42/index.html#cell-ls42-07">42장 · compare로 같은 최종 질문을 두 구현에 보내기</a></li>
</ol></section>`);

insertAfterMain(update, `<section class="edition-group" id="practice-inputs"><h2>11월 27일 · 전반부 실습 입력과 결과 개정</h2><p><a href="../pre-mid/reading-guide.html">1~42장 전체 개정 본문과 실습 열기</a>. 1~5장은 문법과 디자인 패턴 두 경로에서 고른 뒤, 각 장의 코드와 결과를 확인할 수 있습니다.</p></section>`);

insertAfterMain(update, `<section class="edition-group" id="langgraph-intro"><h2>11월 27일 · 33장 LangGraph 입문</h2><p><a href="../chapter33/index.html#cell-graph-33-00">LangGraph의 역할과 상태·노드·간선</a>을 먼저 읽고, <a href="../chapter33/index.html#cell-graph-33-07">두 노드가 연결된 그림과 실행 코드</a>를 대조합니다.</p></section>`);

const earlyPractice = [
  ...Array.from({length: 5}, (_, i) => ['python-basics', 'a0' + (i + 1) + '-save-goal']),
  ['team-git', 'git-case-save-goal'], ['team-git', 'git-verify-case-goal'],
  ['prompt-workshop', 'sdk08-save-goal'], ['prompt-workshop', 'sdk09-open-goal'],
  ['prompt-workshop', 'sdk10-open-goal'], ['chat-workshop', 'chat11-read'],
  ['chat-workshop', 'chat12-prepare-goal'], ['chat-workshop', 'chat13-transfer'],
];
const practiceChanges = Array.from({length: 116}, (_, i) => {
  const n = i + 1;
  const early = earlyPractice[i];
  const chapter = chapterPath(n);
  const pathname = early ? 'pre-mid/' + early[0] + '/index.html' : chapter;
  const anchor = early ? 'cell-' + early[1] : n <= 24 ? 'cell-carry-' + n + '-0'
    : n <= 42 ? 'cell-cum-input-title' : n <= 52 || n >= 86 ? 'team-case'
    : n <= 67 ? 'desk-lab' : 'service-practice';
  const page = readFileSync(join(output, pathname), 'utf8');
  if (!page.includes('id="' + anchor + '"')) throw new Error(pathname + '#' + anchor);
  const heading = (page.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)?.[1] ?? '').replace(/<[^>]+>/g, '').trim();
  const label = early ? revised[i].title : heading.replace(/^\d+\s*[장일]\s*[·.\-]?\s*/, '');
  const second = n <= 5 ? ' · <a href="../pre-mid/python-patterns/index.html#cell-b0' + n + '-save-goal">디자인 패턴</a>' : '';
  return '<li><a href="../' + pathname + '#' + anchor + '">' + n + '장 · ' + label + '</a>' + second + '</li>';
});
insertAfterMain(update, '<section class="edition-group" id="cumulative-practice"><h2>11월 27일 · 1~116장 누적 실습</h2><p>앞 장에서 만든 파일을 열고 새 기능을 적용하는 절입니다. 프로젝트 장에는 팀이 바꾸어 쓸 완성 예시와 다시 시작할 파일이 있습니다.</p><ol>' + practiceChanges.join('') + '</ol></section>');
