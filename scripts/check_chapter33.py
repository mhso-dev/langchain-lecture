"""Verify chapter 33 in two independent local kernels. No model account is needed."""
import argparse
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys

from ipykernel.inprocess.manager import InProcessKernelManager
from lxml import html
import nbformat

CHAPTER = Path(__file__).resolve().parents[1] / "site" / "chapter33"
TASKS = {"code-4", "code-8", "code-9", "code-10"}


def check_model_handoff(namespace):
    """Supply model decisions and check which messages the answer writer receives."""
    from langchain_core.messages import AIMessage

    class ScriptedChat:
        def __init__(self, decision):
            self.decision = decision
            self.answer_inputs = []

        def bind_tools(self, tools):
            assert tools == [namespace["search_documents"]]
            from langchain_core.runnables import RunnableLambda

            def respond(messages):
                assert [message.type for message in messages] == ["human"]
                return self.decision

            return RunnableLambda(respond)

        def invoke(self, messages):
            self.answer_inputs.append(messages)
            return AIMessage(content="근거를 읽었습니다.")

    ask = namespace["ask_library"]
    greeting = ScriptedChat(AIMessage(content="안녕하세요!"))
    answer, history = ask("안녕하세요!", greeting)
    assert answer.content == "안녕하세요!"
    assert [m.type for m in history] == ["human", "ai"] and not greeting.answer_inputs
    search = ScriptedChat(namespace["request"])
    answer, history = ask("대출 기간은?", search)
    assert search.answer_inputs == [history] and answer.content == "근거를 읽었습니다."
    assert [m.type for m in history] == ["human", "ai", "tool"]
    assert (history[-1].tool_call_id, history[-1].artifact[0]["id"]) == ("search-1", "library-1")


def verify(mode):
    nb = nbformat.read(CHAPTER / "chapter33.ipynb", as_version=4)
    nbformat.validate(nb)
    page = html.parse(CHAPTER / "index.html")
    articles = {"code-" + a.get("data-cell"): a for a in page.xpath('//article[@data-cell]')}
    assert {k for k, a in articles.items() if a.get("data-task") == "1"} == TASKS
    kernel = InProcessKernelManager()
    kernel.start_kernel()
    count = 0
    try:
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            count += 1
            source = cell.source
            expected = "".join(o.text for o in cell.outputs if o.output_type == "stream").rstrip("\n")
            article = articles.get(cell.id)
            if article is None:
                assert cell.id == "guided-setup-code"
            else:
                assert source == article.xpath('string(./figure/pre/code)')
                web_output = article.xpath('string(.//div[@class="output"]/pre)')
                if cell.id in TASKS:
                    assert not expected
                    details = article.xpath('./details[not(@open)]')[0]
                    solution = html.fromstring(nb.cells[idx + 1].source)
                    answer_code, answer_output = solution.xpath('./pre/code/text()')
                    assert answer_code == details.xpath('string(./figure/pre/code)')
                    assert answer_output == web_output
                    if mode == "solutions":
                        source, expected = answer_code, answer_output
                else:
                    assert expected == web_output
            with redirect_stdout(StringIO()) as stream:
                outcome = kernel.kernel.shell.run_cell(source, silent=True)
            outcome.raise_error()
            assert stream.getvalue().rstrip("\n") == expected, (cell.id, stream.getvalue(), expected)
        check_model_handoff(kernel.kernel.shell.user_ns)
    finally:
        kernel.shutdown_kernel()
    print(f"{mode}: {count} kernel cells, {len(articles)} HTML examples, {len(TASKS)} answers, 2 model handoff paths")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("starter", "solutions"))
    mode = parser.parse_args().mode
    if mode:
        verify(mode)
    else:
        for case in ("starter", "solutions"):
            subprocess.run([sys.executable, __file__, case], check=True)
