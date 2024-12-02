import re

from ..types import Test, Result


class Contrast(Test):
    """
    Тест для проверки контрастности текста на странице в соответствии с национальными стандартами.
    """

    NAME = "Контраст текста"
    DESCRIPTION = """информация, размещаемая на официальном сайте, соответствует 
критериям оптимальной контрастности, предусмотренным национальным стандартом Российской Федерации"""
    DEFIANCE = "Недостаточная контрастность текста"
    RECOMMENDATION = """Обеспечьте контрастность 4.5:1 для обычного текста и 3:1 для крупного текста."""

    async def run(self):
        """
        Выполняет проверку контрастности текста на странице.

        Использует JavaScript для получения информации о цветах фона и текста
        и вычисляет коэффициент контрастности в соответствии с рекомендациями.

        Returns:
            Result: Результат теста с указанием процента элементов, соответствующих требованиям.
        """
        uuids = await self._execute_js_file("js/contrast.js")
        total = len(uuids)
        with_right_contrast = 0
        for uuid in uuids:
            result = await self._execute_js_file(
                "js/get-info.js", self._page.locator(f"[AccessScan='{uuid}']")
            )
            if not isinstance(result, list) or len(result) != 2:
                continue
            background_color, text_color = map(self.__parse_rgb, result)
            L1 = self.__calculate_relative_luminance(text_color)
            L2 = self.__calculate_relative_luminance(background_color)
            if L1 < L2:
                L1, L2 = L2, L1
            contrast_ratio = (L1 + 0.05) / (L2 + 0.05)
            if contrast_ratio >= 4.5:
                with_right_contrast += 1
        if not total:
            total = 1
            with_right_contrast = 1
        return Result(
            Contrast,
            (with_right_contrast / total) * 100,
        )

    def __parse_rgb(self, color_str: str) -> tuple[int, int, int]:
        """
        Преобразует строку RGB или RGBA в кортеж (R, G, B).

        Args:
            color_str (str): Строка цвета в формате "rgb(r, g, b)" или "rgba(r, g, b, a)".

        Returns:
            tuple[int, int, int]: Кортеж значений RGB. Если строка некорректна, возвращает (255, 255, 255).
        """
        match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
        if not match:
            return (255, 255, 255)
        return tuple(map(int, match.groups()))

    def __calculate_relative_luminance(self, color: tuple[int, int, int]) -> float:
        """
        Вычисляет относительную яркость цвета в соответствии с формулой W3C.

        Args:
            color (tuple[int, int, int]): Кортеж значений RGB.

        Returns:
            float: Относительная яркость цвета.
        """
        RsRGB = color[0] / 255
        GsRGB = color[1] / 255
        BsRGB = color[2] / 255

        R = RsRGB / 12.92 if RsRGB <= 0.03928 else ((RsRGB + 0.055) / 1.055) ** 2.4
        G = GsRGB / 12.92 if GsRGB <= 0.03928 else ((GsRGB + 0.055) / 1.055) ** 2.4
        B = BsRGB / 12.92 if BsRGB <= 0.03928 else ((BsRGB + 0.055) / 1.055) ** 2.4

        return 0.2126 * R + 0.7152 * G + 0.0722 * B
