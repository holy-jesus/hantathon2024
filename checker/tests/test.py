from typing import Any
from pathlib import Path

import aiofiles
import aiofiles.os as os
from playwright.async_api import Browser, Page


class Test:
    NAME: str
    DESCRIPTION: str

    def __init__(self, browser: Browser, page: Page) -> None:
        self._browser = browser
        self._page = page

    async def run(self) -> bool:
        raise NotImplementedError

    async def __execute_js_file(self, name: str, arg=None) -> Any | None:
        file = Path() / name

        if not (await self.__check_path(file)):
            return None

        async with aiofiles.open(file, "r") as f:
            return await self._page.evaluate(f.read(), arg)

    async def __check_path(self, path: Path) -> bool:
        return (
            await os.path.exists(path)
            and await os.path.isfile(path)
            and not await os.path.islink(path)
            and await os.path.isdir(path.parent)
            and path.parent.name == "js"
            and path.name.split(".")[-1] == "js"
        )
