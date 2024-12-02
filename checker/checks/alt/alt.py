from ..types import Test, Result


class Alt(Test):
    """
    Тест для проверки наличия описания у изображений на странице.

    NAME: Название теста.
    DESCRIPTION: Описание теста, поясняющее его цель и соответствие требованиям доступности.
    """

    NAME = "Описание картинок"
    DESCRIPTION = """Тест проверяет, что изображения на сайте имеют атрибуты `alt` 
или эквивалентные текстовые описания для обеспечения доступности."""
    DEFIANCE = "Нетекстовый элемент на веб-странице не содержит атрибута alt с текстовым описанием."
    RECOMMENDATION = """Убедитесь, что все изображения и графические элементы имеют атрибут alt с 
описанием. Обратите внимание, что пустой атрибут alt (alt="") можно использовать только для декоративных элементов."""

    async def run(self):
        """
        Выполняет проверку наличия описаний (атрибутов `alt`) у изображений на странице.

        Использует JavaScript для подсчета:
        - общего количества изображений на странице,
        - количества изображений с атрибутом `alt` или аналогичным.

        Если изображений нет, возвращается результат, считающий тест успешным.

        Returns:
            Result: Результат теста с указанием процента изображений, имеющих описание.
        """
        result = await self._execute_js_file("js/alt.js")

        # Проверяем, что результат корректен и содержит два значения: общее количество и количество с описанием
        assert isinstance(result, list) and len(result) == 2
        total, xpaths = result
        len_with_alt = total - len(xpaths)
        if not total:  # Если изображений нет, считаем, что все корректно
            total = 1
            len_with_alt = 1
        final_score = (len_with_alt / total) * 100
        if final_score != 100.0:
            self._report.add_defiance(self.DEFIANCE)
            self._report.add_recommendation(self.RECOMMENDATION)
            self._report.add_xpaths(xpaths)
        return Result(Alt, final_score)
