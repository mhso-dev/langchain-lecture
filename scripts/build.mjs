import { execFileSync } from 'node:child_process';
import { cpSync, mkdirSync, readFileSync, readdirSync, rmSync } from 'node:fs';
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
const retiredFiles = new Set(['.DS_Store', 'three.min.js', 'pdf-layers.js', 'pdf-layers.css', 'chunk-lab.html']);
function publishable(path) {
  return !retiredFiles.has(basename(path)) && !/\.(?:mp4|webm|gif|png|jpe?g|webp)$/i.test(path);
}
cpSync(source, output, { recursive: true, filter: publishable });

for (const chapter of chapters) {
  const notebook = JSON.parse(readFileSync(join(source, chapter, chapter + '.ipynb'), 'utf8'));
  if (notebook.nbformat !== 4 || !notebook.cells.length) throw new Error(chapter + ' 노트북 오류');
}
execFileSync('python3', [fileURLToPath(new URL('../daily-labs/generate.py', import.meta.url)), output], { stdio: 'inherit' });
execFileSync('python3', [fileURLToPath(new URL('./course_navigation.py', import.meta.url)), output], { stdio: 'inherit' });
console.log(chapters.length + '개 장과 학생 노트북을 dist에 생성했습니다.');
execFileSync('python3', [fileURLToPath(new URL('./topic_reader.py', import.meta.url)), output], { stdio: 'inherit' });
