from ..test import Test


class Buttons(Test):
    async def run(self):
        result = await self._execute_js_file("js/buttons.js")
        return result
