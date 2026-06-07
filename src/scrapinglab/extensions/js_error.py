from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Dialog,
)

class JSError(BaseExtension):
    url = 'https://the-internet.herokuapp.com/javascript_error'

    async def run(self, page: Page) -> None:
        page.on('pageerror', self._handle_error)
        await page.goto(self.url)
    
    async def _handle_error(self, error: Exception) -> None:
        self.logger.info(
            f'An exception within the page is detected.'
            f' Error: {error}')
        