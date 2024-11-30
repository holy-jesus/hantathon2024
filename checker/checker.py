from playwright.async_api import async_playwright
from loguru import logger

from checks import Test, tests


class Checker:
    def __init__(self) -> None:
        self.manager = async_playwright()

    def get_available_tests(self) -> tuple[Test]:
        return tests

    async def run_tests(self, url: str, tests: list[Test] = None) -> list:
        logger.info(f"Начинаю проводить тесты для {url}")
        if not tests:
            tests = self.get_available_tests()
        logger.info(
            f"Буду проводить следующие тесты: {', '.join(test.NAME for test in tests)}"
        )
        async with self.manager as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            results = []
            for test in tests:
                logger.info(f'Начинаю тест "{test.NAME}"')
                try:
                    test: Test = test(browser, page)
                    results.append(await test.run())
                    logger.debug(f'Тест "{test.NAME}" завершен.')
                except Exception as e:
                    logger.error(f'Произошла ошибка при обработке теста "{test.NAME}"')
                    logger.exception(e)
        return results
