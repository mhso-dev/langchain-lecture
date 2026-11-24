"""5일 학생이 작성한 CSV 세 개를 원장과 대조합니다. 사용법: python check_shift.py 출력폴더"""
import csv
from pathlib import Path
import sys
from shift_reference import reconcile

def read(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as source:
        table = csv.DictReader(source)
        missing = set(fields) - set(table.fieldnames or [])
        if missing:
            raise ValueError(f"{path.name}에 없는 열: {sorted(missing)}")
        return list(table)

def check(directory, source):
    journal, held, states = reconcile(read(source, ("event","ticket","branch","kind","minutes")))
    actual = read(directory/"journal.csv",("line","event","ticket","branch","kind","minutes"))
    wanted = [{k:("" if v is None else str(v)) for k,v in r.items()} for r in journal]
    def select(rows,fields):
        return sorted(tuple(r[k] for k in fields) for r in rows)
    def compare(label, expected, observed):
        if expected != observed:
            raise ValueError(f"{label} 불일치\n기대 {expected}\n실제 {observed}")
    compare("정상 이력",select(wanted,wanted[0]),select(actual,wanted[0]))
    actual = read(directory/"review.csv",("line","event","reason"))
    expected = [dict(r,line=str(r["line"])) for r in held]
    compare("검토 이력",select(expected,expected[0]),select(actual,expected[0]))
    actual = read(directory/"queue.csv",("ticket","branch"))
    branches = {r['ticket']:r['branch'] for r in journal}
    compare("대기열",sorted((t,branches[t]) for t,s in states.items() if s != 'close'),
            sorted((r['ticket'],r['branch']) for r in actual))
    print(f"정상 {len(journal)} · 검토 {len(held)} · 대기 {len(actual)} 확인")

if __name__ == "__main__":
    check(Path(sys.argv[1]),Path(__file__).with_name("shift.csv"))
