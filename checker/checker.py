import asyncio

from playwright.async_api import async_playwright


# async def main():
#     async with async_playwright() as p:
#         browser = await p.firefox.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto("https://playwright.dev/python/docs/library")
#         print(await page.title())
#         await asyncio.sleep(10)
#         await browser.close()


class Checker:
    def __init__(self) -> None:
        self.manager = async_playwright()

    async def get_available_checks(self):
        pass




if __name__ == "__main__":
    asyncio.run(main())
