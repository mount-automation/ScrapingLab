import asyncio
from playwright.async_api import (
    Page,
    Dialog,
    Locator,
)
from .core import BaseExtension

class ContextMenu(BaseExtension):
    url = 'https://the-internet.herokuapp.com/context_menu'

    async def run(self, page: Page) -> None:
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

    async def activate_context_menu(self, page: Page) -> bool:
        page.once('dialog', self.dialog_handler)
        hotspot: Locator = page.locator("#hot-spot")
        await hotspot.click(button='right')
        return True