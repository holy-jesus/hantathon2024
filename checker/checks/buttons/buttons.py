from ..types import Test, Result


class Buttons(Test):
    """
    Тест для проверки наличия доступного описания у кнопок на странице.

    NAME: Название теста.
    DESCRIPTION: Описание теста, поясняющее его цель и соответствие требованиям доступности.
    """

    NAME = "Описание кнопок"
    DESCRIPTION = """нетекстовая информация, размещаемая на официальном сайте, 
представлена в альтернативной версии, доступной для чтения при помощи вспомогательных 
технологий, включая программы экранного доступа."""
    DEFIANCE = "Отсутствуют текстовые метки и инструкции для полей форм ввода."
    RECOMMENDATION = (
        "Обеспечьте наличие текстовых меток и инструкций для всех полей ввода."
    )

    async def run(self):
        """
        Выполняет проверку наличия описаний у кнопок на странице.

        Использует JavaScript для получения информации о кнопках и подсчета:
        - общего количества кнопок,
        - количества кнопок с атрибутом `aria-label` или аналогичным.

        Если кнопок нет, возвращается результат, считающий тест успешным.

        Returns:
            Result: Результат теста с указанием процента кнопок, имеющих описание.
        """
        result = await self._execute_js_file("js/buttons.js")

        # Проверяем, что результат корректен и содержит два значения: общее количество и количество с описанием
        assert isinstance(result, list) and len(result) == 2
        total, xpaths = result
        without_aria_label = len(xpaths)
        if not total:
            total = 1
            without_aria_label = 1
        final_score = 100 - ((without_aria_label / total) * 100)
        if final_score != 100.0:
            self._report.add_defiance(self.DEFIANCE)
            self._report.add_recommendation(self.RECOMMENDATION)
            self._report.add_xpaths(xpaths)
        return Result(
            Buttons,
            final_score,
        )
