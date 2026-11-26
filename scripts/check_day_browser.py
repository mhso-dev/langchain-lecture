"""Exercise the static reader at mobile and desktop widths in the build job."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1] / "dist"
with sync_playwright() as browser_api:
    browser = browser_api.chromium.launch(channel="chrome")
    for width in (390, 1280):
        page = browser.new_page(viewport={"width":width, "height":850})
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
        page.close()
        print(f"{width}px · 42→43→85→86→120일 이동")
    browser.close()
