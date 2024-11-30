from ..test import Test


class Zoom(Test):
    NAME = "Масштабирование"
    DESCRIPTION = """текстовая информация, размещаемая на официальном сайте, масштабируется 
не менее чем на 200 процентов от исходного масштаба интернет-страницы без применения 
вспомогательных технологий, без потери функциональности и без появления горизонтальной полосы прокрутки;"""

    async def run(self):
        await self._execute_js_file("js/zoom.js", arg=2.0)

        result = await self._execute_js_file("js/has-horizontal-scrollbar.js")
        assert isinstance(result, bool)

        await self._execute_js_file("js/zoom.js", arg=1.0)
        return not result
