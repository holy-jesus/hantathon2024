import asyncio

from checker import Checker


async def main():
    checker = Checker()
    await checker.run_tests("https://www.google.com/")


if __name__ == "__main__":
    asyncio.run(main())
