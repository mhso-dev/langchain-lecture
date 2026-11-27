"""수업 ZIP의 자료와 학생이 저장한 장별 작업 결과를 구분한다."""
import json
from pathlib import Path


def read_previous(root, chapter):
    personal = root / "my-course" / "workflow" / f"chapter{chapter}.json"
    example = Path(__file__).with_name("examples") / f"chapter{chapter}.json"
    source = personal if personal.is_file() else example
    print(("내 작업 · " if source == personal else "교재 복귀 예시 · ") + source.name)
    return json.loads(source.read_text(encoding="utf-8"))


def save_record(root, chapter, record):
    path = root / "my-course" / "workflow" / f"chapter{chapter}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(path.relative_to(root).as_posix())
