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
    for n in (1, 9, 14, 24, 28, 32, 33, 38, 41, 42):
        page.goto(f"{base}/chapter{n:02}/index.html")
        page.wait_for_selector("main article")
        if page.locator("figure[data-workflow]").count():
            page.wait_for_function("Array.from(document.querySelectorAll('figure[data-workflow]')).every(f=>f.querySelector('svg'))")
        answer = page.locator("article details").last
        answer.locator("summary").click()
        assert answer.get_attribute("open") is not None, n
        dims = page.evaluate("""() => ({
          width: document.documentElement.scrollWidth,
          viewport: innerWidth,
          body: parseFloat(getComputedStyle(document.querySelector('article p')).fontSize)
        })""")
        assert dims["width"] <= dims["viewport"] + 1 and dims["body"] >= 16, (n, dims)
    print(f"{width}px 목차 검색, 장 이동, 답안 펼치기, 그래프 표시, 본문 폭 확인")


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
