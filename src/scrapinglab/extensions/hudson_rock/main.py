from playwright.async_api import (
    Page,
    Browser,
    BrowserContext,
)
from ..core import BaseExtension

class FortiBleedScraper(BaseExtension):
    url = 'https://www.hudsonrock.com/fortinet'



    async def run(self, page: Page) -> None:
        await page.goto(url=self.url)