from ..types import Test, Result


class Buttons(Test):
    NAME = "Описание кнопок"
    DESCRIPTION = """нетекстовая информация, размещаемая на официальном сайте, 
представлена в альтернативной версии, доступной для чтения при помощи вспомогательных 
технологий, включая программы экранного доступа"""

    async def run(self):
        result = await self._execute_js_file("js/buttons.js")

        assert isinstance(result, list) and len(result) == 2
        total, with_aria_label = result
        if not total:
            total = 1
            with_aria_label = 1
        return Result(
            Buttons,
            (with_aria_label / total) * 100,
        )
