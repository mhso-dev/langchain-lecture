# AI 엔지니어링 교재

일반 수업 75장과 프로젝트 41장을 교육일 순서대로 읽는 학생용 사이트다. 목차는 `/`, 각 장은 `/chapter01/`부터 `/chapter116/`까지 독립된 주소를 쓴다. 각 장의 제목과 목차에는 실습에서 쓰는 개념·문법·API 이름을 표시한다.

## 한 장 수정하기

교육 내용을 고칠 때는 [노트북 중심 개편 계획](reports/notebook-first-plan.md)과 [116장 작업표](reports/notebook-revision-map.md)에서 그 장의 입력 자료, 학생이 직접 작성할 코드나 문서, 확인할 결과를 먼저 찾는다.

| 내용 | 수정할 파일 |
| --- | --- |
| 목차의 제목·분류·검수 상태 | `site/index.html` |
| 학생이 읽는 설명·예시·접이식 풀이 | `site/chapterNN/index.html` |
| 예제 코드와 셀 출력 | 같은 폴더의 `chapterNN.ipynb` |
| 무음 개념 영상 | 해당 절의 `visual-*.mp4`, `detail-*.mp4` 또는 `concept.mp4`와 노트북에 첨부한 GIF |
| 공통 디자인·조작·이미지·Three.js | `site/assets/` |
| 이전·다음 장 탐색과 사이트 빌드 | `scripts/build.mjs` |

Three.js 실험의 입력과 계산은 `site/assets/practice-space.js`에 있다. 실험이 있는 장에서는 `#practice-space`로 바로 이동할 수 있다. 무음 영상은 개념을 배우는 절에서 자동 반복 재생된다. [장별 시각 자료 검토 기록](reports/visual-lessons.md)에서 각 장면의 위치와 예시를 확인할 수 있다. 새 영상의 작화와 웹·노트북 반영 스크립트는 `artwork/visual_lessons/`에 있다.

## 확인하기

Node.js 22 이상과 Python 3.9 이상에서 실행한다. 추가 패키지 설치는 필요 없다.

```sh
node scripts/build.mjs
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

브라우저에서 `http://localhost:8000/`을 연다. 검사는 116개 장과 노트북, 실제 파일 경로와 HTML 앵커를 대조한다. 셀 실행 여부와 수업 내용의 교육 검수는 해당 장의 변경 기록에 따로 적는다.

## 변경과 배포

한 작업을 한 브랜치와 PR로 묶는다. 커밋 제목에는 장 번호나 공통 기능을 적는다. 예를 들어 `교재(21장): 청크 경계 실험의 출력 설명 수정`처럼 작성한다. PR에는 바꾼 이유, 영향받는 장과 노트북, 실행한 검사, 확인이 남은 항목을 적는다.

Vercel에서 이 저장소를 연결하고 운영 브랜치를 `main`으로 사용한다. PR의 Preview에서 장 주소·노트북 다운로드·바뀐 조작을 확인한 뒤 병합한다. 운영 배포는 Git SHA와 실제 교재 주소로 확인한다. 되돌릴 때는 해당 PR을 revert하고 같은 검사를 거친다. 빌드 결과인 `dist/`는 Git 추적에서 제외한다.

## 최초 이관

2026년 11월 23일판 단일 HTML(102,132,697바이트)에서 장별 본문·학생 노트북·시각 자료를 분리했다. 원문에 있던 교육 검수 상태는 각 장에 표시한다. 개발용 기록과 강사 전용 자료는 상위 강의 프로젝트에서 관리한다.

[제목·실습·영상의 116장 개정 기록](reports/concept-edition.md)

[장별 본문 개정과 워크플로 영상 목록](https://langchain-lecture.vercel.app/updates/)에는 이번에 바뀐 116개 장의 실제 절과 영상으로 이동하는 링크가 있다. 본문 설명은 관련 셀에 배치하고 과제 풀이만 접는다. 노드·간선·예제 상태의 원본은 `artwork/workflow_lessons/unit*.py`에 있다. 같은 경로를 웹에서는 MP4로, 노트북에서는 내장 GIF로 읽을 수 있다.
