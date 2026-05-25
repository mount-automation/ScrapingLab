import logging
import asyncio
from logging import Logger
from playwright.async_api import (
    Page,
    Dialog,
    Browser,
    Locator,
    BrowserContext,
)

class ContextMenu:
    def __init__(self, browser: Browser|None = None) -> None:
        self.browser: Browser = browser
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.url: str = 'https://the-internet.herokuapp.com/context_menu'
    
    async def init_extension(self) -> None:
        page: Page
        context: BrowserContext
        async with (
            await self.browser.new_context() as context,
            await context.new_page() as page,
        ):
            await page.goto(self.url)
            if await self.activate_context_menu(page=page):
                self.logger.info('ContextMenu module done...')

    async def dialog_handler(self, dialog: Dialog) -> None:
        self.logger.info(
            f'Alert popup message captured:\n'
            f'"{dialog.message}"\n'
        )
        await asyncio.sleep(1.5)
        self.logger.info('Accepting alert popup...')
        await dialog.accept()

    async def activate_context_menu(self, page: Page|None = None) -> bool:
        page.once('dialog', self.dialog_handler)
        hotspot: Locator = page.locator("#hot-spot")
        await hotspot.click(button='right')
        return True