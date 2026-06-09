import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Locator,
    Response,
)
from .shifting_page import ShiftingPage

class ShiftingImage(ShiftingPage):
    async def proceed(self) -> None:
        page: Page = await self.init_page()
        link_list = await page.get_by_role('link', name='click here').all()
        for link in link_list:
            self.logger.info(f'{await link.get_attribute('src')}')