import inspect
from typing import TYPE_CHECKING, Any
from pathlib import Path

import aiofiles
import aiofiles.os as os
from playwright.async_api import Browser, Page
from loguru import logger

if TYPE_CHECKING:
    from .result import Result
    from ...report import Report


class Test:
    """
    Базовый класс для тестов. Определяет общую структуру и методы для выполнения тестов.
    """

    NAME: str  # Название теста
    DESCRIPTION: str  # Описание теста
    DEFIANCE: str  # Нарушение, которое тест проверяет
    RECOMMENDATION: str  # Рекомендация для устранения нарушения

    def __init__(self, browser: Browser, page: Page, report: "Report") -> None:
        """
        Инициализирует тест.

        Args:
            browser (Browser): Экземпляр браузера Playwright.
            page (Page): Страница браузера, на которой будет выполняться тест.
        """
        self._browser = browser
        self._page = page
        self._report = report

    async def run(self) -> "Result":
        """
        Запускает тест. Этот метод должен быть реализован в подклассах.

        Raises:
            NotImplementedError: Если метод не переопределен в подклассе.

        Returns:
            Result: Результат выполнения теста.
        """
        raise NotImplementedError

    async def _execute_js_file(self, name: str, target=None, arg=None) -> Any | None:
        """
        Выполняет JavaScript код из указанного файла.

        Args:
            name (str): Имя файла с JavaScript кодом.
            target (optional): Объект для выполнения JS (по умолчанию `self._page`).
            arg (optional): Аргументы, передаваемые в скрипт.

        Returns:
            Any | None: Результат выполнения скрипта или None, если файл не найден.
        """
        if target is None:
            target = self._page

        logger.trace(f"Запускаю JS файл {name}, target={target}")

        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        module = inspect.getmodule(caller_frame)

        if module and module.__file__:
            file = Path(module.__file__).parent / name
        else:
            raise RuntimeError("Не удалось определить путь к модулю")

        if not (await self._check_path(file)):
            logger.error(f"Не смог найти JS файл: {name}")
            return None

        async with aiofiles.open(file, "r") as f:
            result = await target.evaluate(await f.read(), arg)
            logger.trace(f"JS скрипт вернул {result}")
            return result

    async def _check_path(self, path: Path) -> bool:
        """
        Проверяет, является ли путь валидным для JavaScript файла.

        Args:
            path (Path): Путь к файлу.

        Returns:
            bool: True, если файл существует, является `.js`, и расположен в папке `js`.
        """
        return (
            await os.path.exists(path)
            and await os.path.isfile(path)
            and not await os.path.islink(path)
            and await os.path.isdir(path.parent)
            and path.parent.name == "js"
            and path.name.split(".")[-1] == "js"
        )
