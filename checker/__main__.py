import asyncio

from checker import Checker
from checks import Buttons


async def main():
    checker = Checker()
    results = await checker.run_tests("https://example.com/", [Buttons])
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
