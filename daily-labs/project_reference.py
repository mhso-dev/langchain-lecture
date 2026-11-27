"""Publish the worked team cases and their notebooks together."""
import json


def project_reference(chapter, encode):
    notebook = chapter / (chapter.name + ".ipynb")
    book = json.loads(notebook.read_bytes())
    for cell in book["cells"]:
        if cell["id"] == "recap":
            source = "".join(cell["source"]).replace("## 돌아보기", "## 프로젝트 인계 기준", 1)
            cell["source"] = source.splitlines(keepends=True)

    page = chapter / "index.html"
    content = show_team_input(chapter, book, page.read_text())
    notebook.write_bytes(encode(book))
    for old, new in (
        ("적용 과제와 인계 기준", "프로젝트 인계 기준"),
        ("실습 노트북과 실행 환경", "프로젝트 참고 노트북"),
        ("수업 노트북 (.ipynb)", "프로젝트 참고 노트북 (.ipynb)"),
    ):
        content = content.replace(old, new)
    page.write_text(content)


# Show the fields used in the chapter's decision, including the failing run in the midterm.
_PREVIEW_FIELDS = {
    43: "question decision", 44: "cases.0.question cases.0.expected",
    45: "cases.2.question documents.p3",
    46: "runs.2.question runs.2.expected runs.2.hits documents.p3",
    47: "runs.2.question runs.2.hits runs.2.candidate documents.p3",
    48: "runs.2.question runs.2.graph_ids runs.2.experiment_ids documents.p3",
    49: "runs.2.question runs.2.experiment_ids runs.2.experiment_visible documents.p3",
    50: "runs.2.question citation_issues runs.2.experiment_ids runs.2.experiment_visible",
    51: "runs.2.question runs.2.fixed_ids runs.2.regression_ok documents.p3",
    52: "manifest.2.question fixes peer_run",
    86: "case_id expected observed", 87: "scenario.question scenario.expected",
    88: "scenarios.1.q scenarios.1.status", 89: "contracts.0.q fields",
    90: "contracts.0.q documents.RULE-A.text", 91: "dataset.0.question dataset.0.expected_page",
    92: "runs.0.question runs.0.expected_page runs.0.actual_page",
    93: "issues.0.question issues.0.mismatch", 94: "paths.0.question paths.0.route",
    95: "prepared.0.text prepared.0.section", 96: "hits.0.text hits.0.source",
    97: "cards.0.answer cards.0.citation", 98: "turns.0.question turns.0.cards.0.answer",
    99: "checks.0.input checks.0.actual", 100: "question request_id attempts outcome",
    101: "question outcome prepared.0.text", 102: "question adapter external_call",
    103: "reply.question reply.sources.0.text reply.sources.0.section",
    104: "alpha.task alpha.target", 105: "view.answer view.sources",
    106: "view.active_request storage notice", 107: "lookup.request lookup.own_rows lookup.other_rows",
    108: "beta.task beta.started beta.success beta.evidence", 109: "answer_review.case answer_review.fact",
    110: "public_error.message visible_keys", 111: "cache_check.same cache_check.hits cache_check.misses",
    112: "regression.spelling regression.local_candidate_ok", 113: "deployment.port deployment.status",
    114: "restore.restore_missing deployment.status", 115: "readme.question readme.answer readme.peer_run",
    116: "scenes.0.question scenes.0.expected scenes.0.locations",
}


def show_team_input(chapter, book, content):
    from html import escape
    from pprint import pformat

    day = int(chapter.name.removeprefix("chapter"))
    filename = chapter.name + "-start.json"
    sample = json.loads((chapter / filename).read_bytes())
    cells = {cell["id"]: cell for cell in book["cells"]}
    intro = "".join(cells["team-input"]["source"])
    note = intro.split("\n\n")[-1]
    table = []
    for path in _PREVIEW_FIELDS[day].split():
        value = sample
        for key in path.split("."):
            value = value[int(key)] if isinstance(value, list) else value[key]
        display = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        table.append((path, display))

    info = "이전 장에서 저장한 팀 기록을 먼저 읽습니다. 기록이 없으면 노트북에 담긴 예시로 시작합니다. 직접 수정한 시작 JSON을 노트북 옆에 두어도 됩니다."
    rows = "\n".join(f"- `{key}`　{value}" for key, value in table)
    cells["team-input"]["source"] = (intro.removesuffix(note) + "**이번 장의 입력 예시**\n\n" + rows + "\n\n" + info).splitlines(True)
    html_rows = "".join(f"<li><code>{escape(k)}</code>　{escape(v)}</li>" for k,v in table)
    intro_start = content.index('<p>이 프로젝트의 노트북')
    intro_end = content.index('</p>', intro_start) + len('</p>')
    content = content[:intro_start] + "<p><strong>이번 장의 입력 예시</strong></p><ul>" + html_rows + "</ul><p>" + info + "</p>" + content[intro_end:]

    sample_code = "sample_record = " + pformat(sample, width=88, sort_dicts=False)
    loader = cells["team-open"]
    old_code = "".join(loader["source"])
    start = old_code.index("if not input_file.is_file():")
    end = old_code.index("print(incoming[", start)
    code = old_code[:start] + (
        'if input_file.is_file():\n'
        '    incoming = json.loads(input_file.read_text(encoding="utf-8"))\n'
        '    print("팀 기록" if input_file == team_file else "교재 예시", input_file.name)\n'
        'else:\n'
        '    incoming = sample_record\n'
        '    print("교재 예시", "노트북 내장")\n'
    ) + old_code[end:]
    loader["source"] = code.splitlines(True)
    sample_cell = {"cell_type": "code", "id": "team-embedded-example", "execution_count": None,
                   "metadata": {"jupyter": {"source_hidden": True}}, "outputs": [],
                   "source": sample_code.splitlines(True)}
    book["cells"].insert(book["cells"].index(loader), sample_cell)
    old_figure = '<figure class="code-block"><pre tabindex="0"><code>' + escape(old_code)
    assert old_figure in content, chapter
    full_example = f'<p><a href="{filename}" download>전체 예시 JSON 받기</a> · 노트북의 준비 셀에도 같은 자료가 들어 있습니다.</p>'
    return content.replace(old_figure, full_example + '<figure class="code-block"><pre tabindex="0"><code>' + escape(code), 1)
