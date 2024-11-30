from ..test import Test


class Alt(Test):
    async def run(self):
        result = await self._execute_js_file("js/alt.js")
        return result
