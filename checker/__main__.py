import asyncio

from checker import Checker
from checks import Document


async def main():
    checker = Checker()
    results = await checker.run_tests(
        "https://www.nalog.gov.ru/rn77/about_fts/fts/coordin/ksinv/8950813/"
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
