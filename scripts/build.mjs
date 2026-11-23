import { cpSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('../site/', import.meta.url));
const output = fileURLToPath(new URL('../dist/', import.meta.url));
const chapters = readdirSync(source).filter(name => /^chapter\d+$/.test(name))
  .sort((a, b) => Number(a.slice(7)) - Number(b.slice(7)));
const chapterName = day => 'chapter' + String(day).padStart(2, '0');
if (chapters.length !== 116 || chapters.some((name, i) => name !== chapterName(i + 1))) {
  throw new Error('교육일 1~116에 대응하는 장 폴더를 확인하세요.');
}
rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });
cpSync(source, output, { recursive: true, filter: path => basename(path) !== '.DS_Store' });

function courseNav(day) {
  const link = (n, text) => '<a href="../' + chapterName(n) + '/index.html">' + text + '</a>';
  const links = ['<a href="../index.html">전체 목차</a>', '<span>' + day + '장</span>'];
  if (day > 1) links.push(link(day - 1, '이전 장'));
  if (day < chapters.length) links.push(link(day + 1, '다음 장'));
  return '<nav class="course-nav" aria-label="교재 탐색">' + links.join(' ') + '</nav>';
}
for (const [index, chapter] of chapters.entries()) {
  const folder = join(source, chapter);
  const notebook = JSON.parse(readFileSync(join(folder, chapter + '.ipynb'), 'utf8'));
  if (notebook.nbformat !== 4 || !notebook.cells.length) throw new Error(chapter + ' 노트북 오류');
  for (const file of readdirSync(folder).filter(name => name === 'index.html')) {
    const template = readFileSync(join(folder, file), 'utf8');
    if (!template.includes('<!-- COURSE_NAV -->')) throw new Error(chapter + ' 탐색 메뉴 위치 누락');
    const page = template.replace('<!-- COURSE_NAV -->', () => courseNav(index + 1));
    writeFileSync(join(output, chapter, file), page);
  }
}
console.log(chapters.length + '개 장과 학생 노트북을 dist에 생성했습니다.');
