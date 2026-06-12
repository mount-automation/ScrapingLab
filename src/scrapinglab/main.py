import logging
import asyncio
from logging import Logger
from asyncio import (
    TaskGroup,
    Semaphore,
)
from playwright.async_api import (
    async_playwright, 
    Browser, 
    Playwright,
)
from scrapinglab import (
    ACTIVE_EXTENSIONS,
    BaseExtension,
)

ACTIVE_EXTENSIONS: list[type[BaseExtension]]
logger: Logger = logging.getLogger(__name__)

async def main_init() -> None:
    p: Playwright
    browser: Browser
    async with (
        async_playwright() as p,
        await p.chromium.launch(headless=False) as browser,
    ):
        try:
            tg: TaskGroup
            semaphore: Semaphore = asyncio.Semaphore(3)
            if not semaphore:
                raise ValueError(
                    'Semaphore object could not be initialised')
            async with (
                asyncio.TaskGroup() as tg,    
            ):
                for Extension in ACTIVE_EXTENSIONS:
                    ext = Extension(browser=browser, semaphore=semaphore)
                    tg.create_task(ext.init_extension())
        except Exception:
            logger.exception('TaskGroup failed execution:')

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    asyncio.run(main_init())

if __name__ == '__main__':
    main()