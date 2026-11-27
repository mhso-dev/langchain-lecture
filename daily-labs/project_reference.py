"""Publish the worked team cases and their notebooks together."""
import json


def project_reference(chapter, encode):
    notebook = chapter / (chapter.name + ".ipynb")
    book = json.loads(notebook.read_bytes())
    for cell in book["cells"]:
        if cell["id"] == "recap":
            source = "".join(cell["source"]).replace("## 돌아보기", "## 프로젝트 인계 기준", 1)
            cell["source"] = source.splitlines(keepends=True)
    notebook.write_bytes(encode(book))

    page = chapter / "index.html"
    content = page.read_text()
    for old, new in (
        ("적용 과제와 인계 기준", "프로젝트 인계 기준"),
        ("실습 노트북과 실행 환경", "프로젝트 참고 노트북"),
        ("수업 노트북 (.ipynb)", "프로젝트 참고 노트북 (.ipynb)"),
    ):
        content = content.replace(old, new)
    page.write_text(content)
