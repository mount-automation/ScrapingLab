from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

class ShadowDom(BaseExtension):
    url = 'https://the-internet.herokuapp.com/shadowdom'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        span: Locator = page.locator('span[slot="my-text"]')
        span_text = await span.inner_text()
        self.logger.info(f'Shadowdom text bypassed: {span_text}')
        table: Locator = page.locator('ul[slot="my-text"]')
        entries: list[Locator] = await table.locator('li').all()
        for entry in entries:
            entry_text: str = await entry.inner_text()
            self.logger.info(f'Shadowdom table bypassed: {entry_text}')