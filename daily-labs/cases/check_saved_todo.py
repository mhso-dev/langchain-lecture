"""85일 영속화 변경의 인수 검사. 사용법: python check_saved_todo.py my-codex-desk"""
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

def check(repo):
    spec = spec_from_file_location("student_todo",repo/"todo.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    save = getattr(module,"complete_and_save",None)
    if not callable(save):
        raise ValueError("todo.py에 complete_and_save(path, item_id)를 구현하세요.")
    source = json.loads((repo/"tasks.json").read_text(encoding="utf-8"))
    assert {1,2,3} <= {r['id'] for r in source}, "시작 셀에서 세 번째 동명 업무를 추가하세요."
    with TemporaryDirectory() as tmp:
        path = Path(tmp)/"tasks.json"
        for selected in (3,2):
            rows = deepcopy(source)
            for row in rows:
                row["done"] = False
            path.write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
            save(path,selected)
            saved = json.loads(path.read_text(encoding="utf-8"))
            for row in rows:
                if row['id'] == selected:
                    row['done'] = True
            assert saved == rows, (selected,saved)
            print(f"재개방: {selected}번만 완료, 순서와 다른 필드 보존")

if __name__ == "__main__":
    check(Path(sys.argv[1]).resolve())
