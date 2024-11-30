from playwright.async_api import async_playwright

from tests import Test, tests


class Checker:
    def __init__(self) -> None:
        self.manager = async_playwright()

    def get_available_tests(self) -> tuple[Test]:
        return tests

    async def run_tests(self, url: str, tests: list[Test] = None) -> list:
        if tests is None:
            tests = self.get_available_tests()
        async with self.manager as p:
            browser = await p.firefox.launch(headless=False)
            page = await browser.new_page()
            await page.goto(url)
            results = []
            for test in tests:
                test: Test = test(browser, page)
                results.append(await test.run())
        return results
