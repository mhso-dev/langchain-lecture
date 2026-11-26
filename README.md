# AI 엔지니어링 교재

학생용 첫 화면은 문제를 중심으로 묶은 일반 단원 15개와 팀 프로젝트·현장 활동 자료 3개다. 각 일반 단원에서 예제, 실패 사례, 변경 과제, 접힌 풀이를 읽고 같은 내용의 노트북을 실행할 수 있다. 진도는 학생의 실행 결과에 맞춰 조절한다. 학사 운영용 120일 수업표는 `/schedule.html`에서, 기존 세부 자료는 원래 주소에서 연다.

주제의 순서와 세부 자료 배치는 `coursebook/units.json`, 통합 본문·코드·출력은 `coursebook/*.ipynb`에 작성한다. 프로젝트와 현장 활동 안내 본문은 같은 JSON의 `sections`에 있다. `python scripts/check_topic_notebooks.py`는 각 노트북을 시작 코드로 실행한 뒤 새 상태에서 정답을 대입해 두 실행의 출력을 검증한다. 각 노트북 첫머리에 커널과 필요한 패키지를 표시한다.

## 한 장 수정하기

일반 수업의 최근 집필·실행 범위는 [75장 전수검수 기록](reports/classroom-review.md)에서 확인한다.

교육 내용을 고칠 때는 [노트북 중심 개편 계획](reports/notebook-first-plan.md)과 [116장 작업표](reports/notebook-revision-map.md)에서 그 장의 입력 자료, 학생이 직접 작성할 코드나 문서, 확인할 결과를 먼저 찾는다.

| 내용 | 수정할 파일 |
| --- | --- |
| 일차별 자료의 제목·분류·검수 상태 | `site/index.html` |
| 학생이 읽는 설명·예시·접이식 풀이 | `site/chapterNN/index.html` |
| 예제 코드와 셀 출력 | 같은 폴더의 `chapterNN.ipynb` |
| 형광펜 해설과 선수 개념 | 해당 예제의 `guided-reading` 및 노트북의 같은 제목 |
| Mermaid 실행 흐름 | 장별 HTML의 `figure[data-workflow]`와 노트북의 Mermaid 블록 |
| 수식과 좌표 | HTML의 MathML·좌표 SVG와 노트북의 LaTeX·좌표 첨부 |
| 공통 디자인·조작과 사이트 빌드 | `site/assets/`, `scripts/build.mjs` |

[장별 개정 목록](site/updates/index.html#guided-edition)에서 해당 장의 예제와 흐름도로 이동한다. 차트 렌더러를 함께 배포하므로 로컬 파일에서도 외부 서비스에 접속할 필요가 없다. 확정한 집필 기준과 검수 범위는 [전수 검수 기록](reports/guided-reading-review.md)에 있다.

## 확인하기

Node.js 22 이상과 Python 3.9 이상에서 실행한다. 추가 패키지 설치는 필요 없다.

```sh
node scripts/build.mjs
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

브라우저에서 `http://localhost:8000/`을 연다. 검사는 116개 장과 노트북, 실제 파일 경로와 HTML 앵커를 대조한다. 셀 실행 여부와 수업 내용의 교육 검수는 해당 장의 변경 기록에 따로 적는다.

일반 수업 오프라인 교재는 빌드 후 다음 명령으로 묶는다. 압축을 풀어 `index.html`을 열면 목차와 노트북 다운로드가 작동한다.

```sh
python3 scripts/package_classroom.py ../deliverables/classroom-75.zip
```

## 변경과 배포

한 작업을 한 브랜치와 PR로 묶는다. 커밋 제목에는 장 번호나 공통 기능을 적는다. 예를 들어 `교재(21장): 청크 경계 실험의 출력 설명 수정`처럼 작성한다. PR에는 바꾼 이유, 영향받는 장과 노트북, 실행한 검사, 확인이 남은 항목을 적는다.

Vercel에서 이 저장소를 연결하고 운영 브랜치를 `main`으로 사용한다. PR의 Preview에서 장 주소·노트북 다운로드·바뀐 조작을 확인한 뒤 병합한다. 운영 배포는 Git SHA와 실제 교재 주소로 확인한다. 되돌릴 때는 해당 PR을 revert하고 같은 검사를 거친다. 빌드 결과인 `dist/`는 Git 추적에서 제외한다.

## 최초 이관

2026년 11월 23일판 단일 HTML(102,132,697바이트)에서 장별 본문·학생 노트북·시각 자료를 분리했다. 원문에 있던 교육 검수 상태는 각 장에 표시한다. 개발용 기록과 강사 전용 자료는 상위 강의 프로젝트에서 관리한다.

[제목·실습·영상의 116장 개정 기록](reports/concept-edition.md)

## 실제 모델과 일일 실습

모델 실습에는 수업 커널의 환경 변수 `OPENAI_API_KEY`가 필요하다. `OPENAI_MODEL`로 도구 호출과 구조화 출력을 지원하는 모델을 지정할 수 있다. SDK 예제에는 openai, LangChain 예제에는 langchain-openai를 설치한다. 자료에서 답을 찾는 순수 함수는 네트워크 없이 별도로 시험할 수 있다. 매일의 연결 개념과 실습은 `daily-labs/extensions.txt`, 6회 Codex 사례는 `daily-labs/codex_studio.py`에서 수정한다. [전체 편성과 실행 검수](reports/live-model-practice.md)
