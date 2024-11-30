from ..types import Test, Result


class Alt(Test):
    NAME = "Описание картинок"
    DESCRIPTION = ""

    async def run(self):
        result = await self._execute_js_file("js/alt.js")
        assert isinstance(result, list) and len(result) == 2
        total, with_alt = result
        if not total:
            total = 1
            with_alt = 1
        return Result(Alt, (with_alt / total) * 100)
