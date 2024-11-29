from ..test import Test



class Zoom(Test):
    NAME = "Масштабирование"
    DESCRIPTION = """текстовая информация, размещаемая на официальном сайте, масштабируется 
не менее чем на 200 процентов от исходного масштаба интернет-страницы без применения 
вспомогательных технологий, без потери функциональности и без появления горизонтальной полосы прокрутки;"""

    async def run(self):
        await self.__execute_js_file("js/zoom.js", 2.0)
        result = await self.__execute_js_file("js/check-horizontal-scrollbar.js")
        await self.__execute_js_file("js/zoom.js", 1.0)
        return result
