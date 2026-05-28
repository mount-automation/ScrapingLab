from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
import asyncio

class ExitIntent(BaseExtension):
    url = 'https://the-internet.herokuapp.com/exit_intent'

    async def run(self, page: Page) -> None:
        await page.goto(self.url, timeout=60000)
        self.logger.info('Initialize mouse start position.')
        await page.mouse.move(640, 400)
        self.logger.info("Moving mouse out of the browser's viewport...")
        await page.mouse.move(640, -10)
        close: Locator = page.get_by_text('Close')
        await asyncio.sleep(1.5)
        self.logger.info('Closing exit intent ad...')
        await close.click()
        self.logger.info('Exit intent ad successfully closed.')
        await asyncio.sleep(1.5)
