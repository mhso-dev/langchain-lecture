"""Exercise the student reading path with desktop and mobile viewport sizes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

DIST = Path(__file__).resolve().parents[1] / "dist"


class QuietServer(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def check_reader(page, base, width):
    page.goto(base)
    assert page.locator("article.card").count() == 116
    assert page.locator("#part-3 article.card").count() == 11
    page.locator("#search").fill("LangSmith")
    assert page.locator("article.card:visible").count()
    routes = [f"chapter{n:02}/index.html" for n in range(1, 117)]
    routes.extend(f"pre-mid/{slug}/index.html" for slug in ("python-basics", "python-patterns"))
    for route in routes:
        page.goto(f"{base}/{route}")
        page.locator("main").first.wait_for()
        figures = page.locator("figure[data-workflow]")
        if figures.count():
            page.wait_for_function("Array.from(document.querySelectorAll('figure[data-workflow]')).every(f=>f.querySelector('svg'))")
        answers = page.locator('main details.notebook-answer, main article details')
        if answers.count():
            answer = answers.last
            summary = answer.locator("summary").first
            summary.focus()
            summary.press("Enter")
            assert answer.get_attribute("open") is not None, route
        assert page.locator('main a[href$=".ipynb"], header a[href$=".ipynb"]').count(), route
        dims = page.evaluate("() => [document.documentElement.scrollWidth, innerWidth]")
        assert dims[0] <= dims[1] + 1, (route, dims)
    workshop = f"{base}/pre-mid/prompt-workshop"
    page.goto(f"{workshop}/index.html#section-day09-1")
    example = page.locator("#cell-brief-to-request")
    assert example.locator("blockquote").is_visible()
    assert "오전 9시 30분" in example.inner_text()
    assert example.locator("a").count() == 0
    page.goto(f"{workshop}/practice.html")
    assert page.locator("article blockquote").first.is_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
    print(f"{width}px · 116개 장과 선택 경로의 본문·노트북 링크·답안 펼치기·그림·페이지 너비 확인")


with ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietServer, directory=str(DIST))) as server:
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="chrome")
            for width in (390, 1180):
                page = browser.new_page(viewport={"width": width, "height": 850})
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                check_reader(page, f"http://127.0.0.1:{server.server_port}", width)
                assert not errors, errors
                page.close()
            browser.close()
    finally:
        server.shutdown()
