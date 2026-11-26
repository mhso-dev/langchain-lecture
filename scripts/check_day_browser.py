"""Exercise the static reader at mobile and desktop widths in the build job."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1] / "dist"
with sync_playwright() as browser_api:
    browser = browser_api.chromium.launch(channel="chrome")
    for width in (390, 1280):
        page = browser.new_page(viewport={"width":width, "height":850})
        page.goto((root/"index.html").as_uri())
        search = page.get_by_role("searchbox")
        search.fill("add_conditional_edges")
        result = page.locator(".card:visible a")
        assert result.count() >= 1
        result.filter(has_text="조건 분기").click()
        assert "/chapter27/" in page.url
        page.get_by_role("link", name="교재 홈", exact=True).first.click()
        search.fill("26장")
        assert result.count() == 1
        result.click()
        page.locator('.integrated-jump a').click()
        assert page.url.endswith("chapter26/index.html#integrated-example")
        section = page.locator("#integrated-example")
        assert section.locator("a[download]").get_attribute("href") == "state-graph.ipynb"
        answer = section.locator(".notebook-answer").first
        answer.locator("summary").click()
        assert answer.locator("pre").first.is_visible()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        page.goto((root/"topics/state-graph/index.html").as_uri()+"#material-27")
        page.wait_for_url("**/chapter27/index.html")
        page.goto((root/"topics/state-graph/index.html").as_uri()+"#read-2")
        page.wait_for_url("**/chapter26/index.html#integrated-read-2")
        assert page.locator("#integrated-read-2").is_visible()
        page.goto((root/"chapter42/index.html").as_uri())
        nav = page.locator("#course-days")
        nav.locator("[rel=next]").click()
        assert "/chapter43/" in page.url
        nav.get_by_text("일차 선택",exact=True).click()
        nav.locator('a[href="../chapter85/index.html"]').click()
        nav.locator("[rel=next]").click()
        assert "/chapter86/" in page.url
        nav.locator("summary").click()
        nav.locator('a[href="../chapter120/index.html"]').click()
        assert "/chapter120/" in page.url and not nav.locator("[rel=next]").count()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        home = (root/"index.html").as_uri()
        for section in ("chapter120", "topics/state-graph"):
            page.goto((root/section/"index.html").as_uri())
            page.get_by_role("link", name="교재 홈", exact=True).last.click()
            assert page.url == home and search.is_visible()
        page.goto((root/"daily/index.html").as_uri()+"#day117")
        page.wait_for_url("**/chapter117/index.html#daily-lab")
        assert page.locator("#daily-lab").get_by_text("입력 자료 준비",exact=True).is_visible()
        page.goto((root/"daily/index.html").as_uri())
        page.wait_for_url((root/"index.html").as_uri())
        page.close()
        print(f"{width}px · 42→43→85→86→120일 이동")
    browser.close()
