import inspect
from typing import TYPE_CHECKING, Any
from pathlib import Path

import aiofiles
import aiofiles.os as os
from playwright.async_api import Browser, Page

if TYPE_CHECKING:
    from .result import Result


class Test:
    NAME: str
    DESCRIPTION: str

    def __init__(self, browser: Browser, page: Page) -> None:
        self._browser = browser
        self._page = page

    def __repr__(self):
        return f"Тест(name={self.NAME})"

    async def run(self) -> "Result":
        raise NotImplementedError

    async def _execute_js_file(self, name: str, target=None, arg=None) -> Any | None:
        if target is None:
            target = self._page

        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        module = inspect.getmodule(caller_frame)

        if module and module.__file__:
            file = Path(module.__file__).parent / name
        else:
            raise RuntimeError("Не удалось определить путь к модулю")

        if not (await self._check_path(file)):
            return None

        async with aiofiles.open(file, "r") as f:
            return await target.evaluate(await f.read(), arg)

    async def _check_path(self, path: Path) -> bool:
        return (
            await os.path.exists(path)
            and await os.path.isfile(path)
            and not await os.path.islink(path)
            and await os.path.isdir(path.parent)
            and path.parent.name == "js"
            and path.name.split(".")[-1] == "js"
        )
