"""노트북을 닫아도 이어 쓸 수 있는 수업 파일과 복귀 예시."""
import json
from pathlib import Path
from uuid import uuid4

EXAMPLES = Path(__file__).parent / "resume"


def save_step(root, name, value):
    folder = root / "my-course" / "rag"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (name + ".json")
    temporary = path.with_name(f".{name}-{uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return path


def load_step(root, name):
    path = root / "my-course" / "rag" / (name + ".json")
    if not path.is_file():
        path = EXAMPLES / (name + ".json")
        print("이전 장 완성 예시 사용:", path.name)
    return json.loads(path.read_text(encoding="utf-8"))


def chat_case(root):
    path = root / "my-course" / "chat-case.json"
    if not path.is_file():
        path = EXAMPLES / "chat-case.json"
        print("13장 완성 예시 사용:", path.name)
    return json.loads(path.read_text(encoding="utf-8"))


def page_id(row):
    return f"{row['source']}#p{row['page']}"
