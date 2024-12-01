from playwright.async_api import async_playwright
from loguru import logger

from .checks import Test, tests


class Checker:
    def __init__(self) -> None:
        """
        Инициализирует объект Checker и создает менеджер Playwright.
        """
        self.manager = async_playwright()

    def get_available_tests(self) -> tuple[Test]:
        """
        Возвращает список всех доступных тестов.

        Returns:
            tuple[Test]: Кортеж доступных тестов, импортированных из модуля checks.
        """
        return tests

    async def run_tests(self, url: str, tests: list[Test] = None) -> list:
        """
        Запускает указанные тесты для заданного URL.

        Args:
            url (str): URL страницы, которую нужно протестировать.
            tests (list[Test], optional): Список тестов, которые нужно выполнить. 
                                          Если не указан, будут выполнены все доступные тесты.

        Returns:
            list: Список результатов выполнения тестов. Каждый результат 
                  зависит от реализации метода `run()` в классе Test.
        """
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
