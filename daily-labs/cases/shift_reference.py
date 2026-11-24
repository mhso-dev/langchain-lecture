"""교대 원장의 감사 이력을 보존하면서 다음 근무자의 대기열을 복원한다."""
import csv
from collections import Counter
from pathlib import Path

def reconcile(rows):
    seen = set()
    journal, held = [], []
    current = {}
    for line, row in enumerate(rows, start=2):
        eid, ticket, branch, kind, raw = (row[k].strip() for k in ('event','ticket','branch','kind','minutes'))
        reason = None
        minutes = None
        if eid in seen:
            reason = 'duplicate'
        elif not branch:
            reason = 'missing_branch'
        elif kind == 'close':
            try:
                minutes = int(raw)
                if minutes < 0:
                    reason = 'negative_minutes'
            except ValueError:
                reason = 'missing_minutes' if not raw else 'invalid_minutes'
        seen.add(eid)
        if reason is None:
            prior = current.get(ticket)
            allowed = {'open': None, 'reopen': 'close'}
            if kind == 'close':
                if prior not in ('open','reopen'):
                    reason = 'invalid_transition'
            elif kind not in allowed or prior != allowed[kind]:
                reason = 'invalid_transition'
        if reason:
            held.append(dict(line=line, event=eid, reason=reason))
            continue
        current[ticket] = kind
        journal.append(dict(line=line, event=eid,ticket=ticket,branch=branch,kind=kind,minutes=minutes))
    return journal, held, current

if __name__ == '__main__':
    with Path(__file__).with_name('shift.csv').open(encoding='utf-8',newline='') as f:
        journal, held, current = reconcile(csv.DictReader(f))
    print('채택 / 검토',len(journal),len(held),Counter(r['reason'] for r in held))
    print('대기열',sorted(k for k,v in current.items() if v != 'close'))
    print('완료 이벤트 시간', [r['minutes'] for r in journal if r['kind']=='close'])
