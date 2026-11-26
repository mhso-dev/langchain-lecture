"""Connect published notebook checksums to their recorded execution job."""
from hashlib import sha256
import json
from pathlib import Path
import re

def publish_results(out):
    evidence=json.loads(Path(__file__).with_name("verified.json").read_text())
    url=f"https://github.com/mhso-dev/langchain-lecture/actions/runs/{evidence['run']}"
    page=out/"index.html"
    source=page.read_text()
    rows=[]
    for record in evidence["chapters"]:
        day=record["day"]
        stem=f"chapter{day:02}"
        notebook=out/stem/(stem+".ipynb")
        if sha256(notebook.read_bytes()).hexdigest()!=record["sha256"]:
            continue
        entry_pattern=rf'(<a href="{stem}/index.html">(?:(?!</a>).)*?<h3>([^<]+)</h3>\s*)<span class="state hold">실행 검증 대기</span>'
        match=re.search(entry_pattern,source,re.S)
        if not match:
            raise ValueError(f"{day}장 실행 표기를 찾을 수 없습니다.")
        title=match[2]
        source=source[:match.start()]+match[1]+'<span class="state verified">학생·풀이 실행 확인</span>'+source[match.end():]
        rows.append(f'<tr><td><a href="../{stem}/index.html">{day}장 · {title}</a></td><td>{record["student"]}</td><td>{record["solution"]}</td><td><a href="{url}/job/{record["job"]}">실행 로그</a></td></tr>')
    page.write_text(source.replace('<p class="notice">','<p class="notice"><a href="execution/index.html">노트북 장별 실행 결과</a></p><p class="notice">',1))
    folder=out/"execution"
    folder.mkdir(exist_ok=True)
    (folder/"index.html").write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>노트북 장별 실행 결과</title><link rel="stylesheet" href="../assets/catalog.css"></head><body><header><a href="../index.html">전체 교재</a><h1>노트북 장별 실행 결과</h1></header><main><p>실행 대기 장의 학생 코드를 빈 작업 폴더에서 순서대로 실행하고, 별도 Python 프로세스에서 풀이를 적용해 다시 실행했습니다. 표의 숫자는 각 경로에서 실제 실행한 코드 셀 수입니다. 배포 노트북 파일이 실행 당시와 일치하는 장을 표시합니다.</p><p>Chroma 재개방, Streamlit 화면 시험, PostgreSQL, Docker와 로컬 재정렬 모델은 준비된 Linux 환경에서 실행했습니다. 계정이 필요한 수업 활동과 학생이 새로 작성할 코드의 결과는 각 과제에서 확인합니다.</p><table><thead><tr><th>장</th><th>학생 셀</th><th>풀이 셀</th><th>기록</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table><p><a href="'+url+'">실행 기록과 장별 출력 파일</a></p></main></body></html>')
