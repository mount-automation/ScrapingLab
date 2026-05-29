from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    FileChooser,
)
import asyncio

class FloatingMenu(BaseExtension):
    url = 'https://the-internet.herokuapp.com/floating_menu'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        link_footer: Locator = page.get_by_role(
            'link', name='Elemental Selenium')
        self.logger.info('Scrolling to the bottom of the page...')
        for _ in range(20):
            await page.mouse.wheel(0, 250)
            await asyncio.sleep(0.15)
        # await link_footer.scroll_into_view_if_needed()
        await page.pause()