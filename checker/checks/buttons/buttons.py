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

        return Result(
            Buttons, total / with_aria_label if all((total, with_aria_label)) else 0
        )
