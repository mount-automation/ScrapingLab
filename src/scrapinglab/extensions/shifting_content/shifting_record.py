from playwright.async_api import (
    Page,
    Locator,
)
from .shifting_page import ShiftingPage

class ShiftingRecord(ShiftingPage):
    async def proceed(self) -> None:
        page: Page = await self.init_page()
        for _ in range(5):
            await self._find_important_information(page=page)
            await self._reload_page(page=page)
        
    async def _find_important_information(self, page: Page) -> None:
        main_div: Locator = page.locator(
            'div.large-6.columns.large-centered')
        text_blob: str = (await main_div.inner_text()).strip()
        text_list = text_blob.split('\n\n')
        for text in text_list:
            if 'Important Information' in text:
                self.logger.info('Important information found this time.')

    async def _reload_page(self, page: Page) -> None:
        await page.reload()
        self.logger.info('Page reloaded')