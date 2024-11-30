import asyncio

from checker import Checker


async def main():
    checker = Checker()
    results = await checker.run_tests("https://github.com/")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
