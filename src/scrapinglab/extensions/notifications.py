from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
import asyncio

class Notifications(BaseExtension):
    url = 'https://the-internet.herokuapp.com/notification_message_rendered'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._check_notification(page=page)
        for _ in range(5):
            await self._load_message(page=page)
            await self._check_notification(page=page)

    async def _load_message(self, page: Page) -> None:
        link: Locator = page.get_by_role('link', name='Click here')
        await link.click()
        self.logger.info('Page refreshed.')
        
    async def _check_notification(self, page: Page) -> None:
        noti: Locator = page.locator('div#flash')
        if await noti.is_visible():
            message: str = (await noti.inner_text()).split('\n')[0]
            self.logger.info(f'{message.strip()}')
            await self._close_notification(page=page)
    
    async def _close_notification(self, page: Page) -> None:
        close_noti: Locator = page.get_by_role("link", name="×")
        await close_noti.click()
        self.logger.info('Notification closed.')