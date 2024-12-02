import asyncio
import argparse

from checker import Checker
from checks import Document


async def main(url: str = None):
    if not url:
        url = "https://example.com/"
    checker = Checker()
    await checker.run_tests(url)
    # print(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AccessScan: автоматизированная проверка доступности веб-сайтов"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=False,
        help="URL веб-сайта для проверки доступности",
        default="https://example.com/",
    )
    args = parser.parse_args()
    url = args.url
    asyncio.run(main(url))
