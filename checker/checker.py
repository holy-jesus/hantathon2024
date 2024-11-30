from playwright.async_api import async_playwright


class Checker:
    def __init__(self) -> None:
        self.manager = async_playwright()

    async def get_available_tests(self):
        pass
