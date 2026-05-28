from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
import asyncio

class EntryAd(BaseExtension):
    url = 'https://the-internet.herokuapp.com/entry_ad'
    
    async def run(self, page: Page) -> None:
        modal_close: Locator = page.get_by_text('Close', exact=True)
        await page.goto(self.url, timeout=60000)

        await modal_close.wait_for(state='visible', timeout=10000)
        self.logger.info('Closing entry ad...')
        
        await modal_close.click()
        self.logger.info('Reloading page...')
        await asyncio.sleep(2)
        await page.reload()
        await asyncio.sleep(2)
        
        header: Locator = page.get_by_role('heading', name='Entry Ad')
        await header.wait_for(state='visible', timeout=10000)

        self.logger.info('Confirming that entry ad is hidden...')
        modal: Locator = page.locator('div#modal')
        await modal.wait_for(state='hidden', timeout=10000)
        self.logger.info('Entry ad is hidden.')


