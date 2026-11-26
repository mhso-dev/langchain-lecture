import { execFileSync } from 'node:child_process';
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
// Keep retired teaching media in the source archive and exclude it from the student site.
const retiredFiles = new Set(['.DS_Store', 'three.min.js', 'pdf-layers.js', 'pdf-layers.css', 'chunk-lab.html', '__pycache__', '.ipynb_checkpoints']);
function publishable(path) {
  return !path.endsWith('.pyc') && !retiredFiles.has(basename(path)) && !/\.(?:mp4|webm|gif|png|jpe?g|webp)$/i.test(path);
}
cpSync(source, output, { recursive: true, filter: publishable });

function courseNav(day) {
  const link = (n, text) => '<a href="../' + chapterName(n) + '/index.html">' + text + '</a>';
  const links = ['<a href="../index.html">전체 목차</a>', '<span>' + day + '장</span>'];
  const previous = day === 53 ? 42 : day - 1;
  const next = day === 42 ? 53 : day + 1;
  if (day > 1) links.push(link(previous, '이전 장'));
  if (day !== 85 && day < chapters.length) links.push(link(next, '다음 장'));
  return '<nav class="course-nav" aria-label="교재 탐색">' + links.join(' ') + '</nav>';
}
for (const [index, chapter] of chapters.entries()) {
  const folder = join(source, chapter);
  const notebook = JSON.parse(readFileSync(join(folder, chapter + '.ipynb'), 'utf8'));
  if (notebook.nbformat !== 4 || !notebook.cells.length) throw new Error(chapter + ' 노트북 오류');
  if (index < 42) continue; // The pre-project reader renders these routes from canonical notebooks.
  for (const file of readdirSync(folder).filter(name => name === 'index.html')) {
    const template = readFileSync(join(folder, file), 'utf8');
    if (!template.includes('<!-- COURSE_NAV -->')) throw new Error(chapter + ' 탐색 메뉴 위치 누락');
    const page = template.replace('<!-- COURSE_NAV -->', () => courseNav(index + 1))
      .replace(/(>(?:\s*))DAY(?:\s*\/)?\s*(\d+)(?: \/ \d+)?(?=\s*(?:\/|<))/g, (_, prefix, n) => prefix + Number(n) + '장')
      .replace(/<span>교육일 (\d+) · (8H|8시간)<\/span>/g, (_, n, hours) => '<span>' + Number(n) + '장 · ' + hours + '</span>');
    writeFileSync(join(output, chapter, file), page);
  }
}
execFileSync('python3', [fileURLToPath(new URL('../daily-labs/generate.py', import.meta.url)), output], { stdio: 'inherit' });
console.log(chapters.length + '개 장과 학생 노트북을 dist에 생성했습니다.');
execFileSync(process.execPath, [fileURLToPath(new URL('./pre_mid_reader.mjs', import.meta.url))], { stdio: 'inherit' });
execFileSync('python3', [fileURLToPath(new URL('./pre_mid_daily.py', import.meta.url))], { stdio: 'inherit' });
