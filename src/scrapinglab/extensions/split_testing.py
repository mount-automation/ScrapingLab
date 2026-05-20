import logging
from logging import Logger
import asyncio
from playwright.async_api import (
    Browser,
    BrowserContext, 
    Page, 
    Locator,
)
class SplitTesting:
    def __init__(self, browser: Browser|None = None) -> None:
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.browser: Browser = browser
        self.url: str = 'https://the-internet.herokuapp.com/abtest'

    async def init_extension(self) -> None:
        context: BrowserContext
        page: Page
        async with (
            await self.browser.new_context() as context, 
            await context.new_page() as page,
        ):
            await page.goto(self.url)
            div: Locator = page.locator('div.example')
            header: Locator = div.get_by_role('heading', level=3)

            await header.wait_for()

            header_text: str = await header.inner_text()
        self._confirm_result(text=header_text)
        await asyncio.sleep(5)
        self.logger.info(f'{self.__class__.__name__} is done...\n')

    def _confirm_result(self, text:str = '') -> None:
        header_text_list: list[str] = [
            'A/B Test Variation 1',
            'A/B Test Control'
        ]
        if text in header_text_list:
            self.logger.info(f'Current header is "{text}" in "{self.url}"...')
        else:
            self.logger.warning(f'"{text}" not found in records...')