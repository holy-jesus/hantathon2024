import re

from ..test import Test


class Contrast(Test):
    async def run(self):
        uuids = await self._execute_js_file("js/contrast.js")
        result = await self._execute_js_file(
            "js/get-colors.js", self._page.locator(f"[AccessScan='{uuids[0]}']")
        )
        assert isinstance(result, list) and len(result) == 2
        background_color, text_color = map(self.__parse_rgb, result)
        L1 = self.__calculate_relative_luminance(text_color)
        L2 = self.__calculate_relative_luminance(background_color)
        if L1 < L2:
            L1, L2 = L2, L1
        contrast_ratio = (L1 + 0.05) / (L2 + 0.05)
        if contrast_ratio < 4.5:
            return False
        return True

    def __parse_rgb(self, color_str: str) -> tuple[int, int, int]:
        """
        Преобразует строку RGB или RGBA в кортеж (R, G, B).
        """
        match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
        if not match:
            return (255, 255, 255)
        return tuple(map(int, match.groups()))

    def __calculate_relative_luminance(self, color: tuple[int, int, int]):
        RsRGB = color[0] / 255
        GsRGB = color[1] / 255
        BsRGB = color[2] / 255

        R = RsRGB / 12.92 if RsRGB <= 0.03928 else ((RsRGB + 0.055) / 1.055) ** 2.4
        G = GsRGB / 12.92 if GsRGB <= 0.03928 else ((GsRGB + 0.055) / 1.055) ** 2.4
        B = BsRGB / 12.92 if BsRGB <= 0.03928 else ((BsRGB + 0.055) / 1.055) ** 2.4

        return 0.2126 * R + 0.7152 * G + 0.0722 * B
