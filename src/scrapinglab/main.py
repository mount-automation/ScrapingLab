import logging
from logging import Logger
import asyncio
from asyncio import TaskGroup
from playwright.async_api import (
    async_playwright, 
    Browser, 
    Playwright,
)
from scrapinglab.extension_1 import Extension1

logger: Logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)

async def main_init() -> None:
    p: Playwright
    browser: Browser
    async with (
        async_playwright() as p,
        await p.chromium.launch(headless=False) as browser,
    ):
        ext_list = [Extension1(browser=browser)]
        try:
            tg: TaskGroup
            async with asyncio.TaskGroup() as tg:
                for ext in ext_list:
                    tg.create_task(ext.init_extension())
        except ExceptionGroup:
            logger.exception('TaskGroup failed execution:')

def main() -> None:
    asyncio.run(main_init())

if __name__ == '__main__':
    main()