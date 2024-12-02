from ..types.test import Test
from ..types.result import Result


class Zoom(Test):
    NAME = "Масштабирование"
    DESCRIPTION = """текстовая информация, размещаемая на официальном сайте, масштабируется 
не менее чем на 200 процентов от исходного масштаба интернет-страницы без применения 
вспомогательных технологий, без потери функциональности и без появления горизонтальной полосы прокрутки;"""
    DEFIANCE = "При увеличении масштаба теряется функциональность и появляется горизонтальная полоса прокрутки."
    RECOMMENDATION = """Обеспечьте масштабирование текста и графика до 200% без потери качества и функциональности. 
Используйте относительные единицы измерения (например, em, rem) вместо абсолютных (px). Тестируйте сайт на 
различных устройствах и разрешениях экрана, чтобы убедиться в отсутствии горизонтальной полосы прокрутки."""

    async def run(self):
        await self._execute_js_file("js/zoom.js", arg=2.0)

        result = await self._execute_js_file("js/has-horizontal-scrollbar.js")
        assert isinstance(result, bool)

        await self._execute_js_file("js/zoom.js", arg=1.0)
        final_score = 100.0 if not result else 0.0
        if final_score != 100.0:
            self._report.add_defiance(self.DEFIANCE)
            self._report.add_recommendation(self.RECOMMENDATION)
        return Result(Zoom, final_score)
