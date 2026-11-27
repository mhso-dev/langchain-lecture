"""Read short examples from the same files shipped with the individual exercises."""
import csv
import json
from html import escape


def assignment_inputs(folder, day):
    questions_for = {
        55: ["Q01"], 57: ["Q01", "Q06", "Q10"], 58: ["Q01", "Q06", "Q10"],
        61: ["Q04"], 62: ["Q04"], 63: ["Q06", "Q01"], 66: ["Q04"],
        117: ["Q01", "Q09"], 118: ["Q03", "Q04", "Q05"], 119: ["Q07"],
    }
    clauses_for = {59: ["R01-1", "R02-1", "R03-1"], 61: ["R02-1"], 62: ["R02-1"],
                   66: ["R01-1", "R02-1"], 117: ["R02-1"], 119: ["E03-1"], 118: ["R01-1", "R02-1", "R04-1"]}
    rows = []
    if day in (53, 55):
        with (folder / "tickets.csv").open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                if day == 53 and row["branch"] == "서울" or day == 55 and row["request_id"] == "T03":
                    rows.append((row["request_id"], f'{row["branch"]} · {row["audience"]} · {row["status"]} · {row["minutes"]}분'))
    if day in (57, 58):
        for skill in ("receipt", "export"):
            lines = (folder / "skills" / skill / "SKILL.md").read_text().splitlines()
            rows.append((lines[0].removeprefix("# "), lines[1]))
    if day in questions_for:
        with (folder / "questions.csv").open(encoding="utf-8", newline="") as stream:
            data = {r["qid"]:r for r in csv.DictReader(stream)}
        for key in questions_for[day]:
            row = data[key]
            rows.append((key, f'{row["question"]} ({row["branch"] or "지점 미기재"} · {row["audience"]} · {row["as_of"]})'))
    if day in clauses_for:
        data = {r["chunk_id"]:r for r in json.loads((folder / "chunks.json").read_bytes())}
        for key in clauses_for[day]:
            row = data[key]
            rows.append((key, f'{row["branch"]} · {row["audience"]} · {row["valid_from"]}~{row["valid_to"]}　{row["text"]}'))
    if day == 118:
        rows.append(("날짜 변형", "Q05 원문은 9월 1일입니다. 비교 셀에서는 가맹점 기준일을 7월 1일로 바꿉니다."))
    if not rows:
        return "", ""
    md = "**이 과제에서 읽을 입력**\n\n" + "\n".join(f"- **{key}**　{text}" for key,text in rows)
    web = "<h3>이 과제에서 읽을 입력</h3><ul>" + "".join(f"<li><strong>{escape(key)}</strong>　{escape(text)}</li>" for key,text in rows) + "</ul>"
    return md, web
