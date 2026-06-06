from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

class InfiniteScrolling(BaseExtension):
    url = 'https://the-internet.herokuapp.com/infinite_scroll'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        paragraph: Locator = page.locator('div.jscroll-added')
        paragraph_amount: int = await paragraph.count()
        target_amount = 10
        await self._scroll_till_target_amount(
            paragraph=paragraph,
            curr_amount=paragraph_amount,
            target_amount=target_amount,)
        
    async def _scroll_till_target_amount(
        self,
        paragraph: Locator,
        curr_amount: int, 
        target_amount: int,) -> None:
        page: Page = paragraph.page
        while target_amount > curr_amount:
            await page.mouse.wheel(delta_x=0, delta_y=500)
            amount: int = await paragraph.count()
            curr_amount = amount
            if target_amount <= amount:
                self.logger.info(
                    f'Target amount ({target_amount}) reached.' 
                    f' Current paragraph amount: {amount}')
                break