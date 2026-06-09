import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Locator,
    Response,
)
from .shifting_page import ShiftingPage

class ShiftingMenu(ShiftingPage):
    async def proceed(self) -> None:
        page: Page = await self.init_page()
        portfolio_link: Locator = page.get_by_role('link', name='Portfolio')
        mode_link: Locator = page.get_by_role(
            'link', name='click here').nth(2)
        await mode_link.click()
        response_url: str = 'https://the-internet.herokuapp.com/portfolio/'
        async with (
            page.expect_response(response_url) as response_info
        ):
            await portfolio_link.evaluate('(element) => element.click()')
        response: Response|None = await response_info.value
        if response:
            self.logger.info('Shifted portfolio link successfully clicked.')
            await page.goto(self.home_url)
            await page.pause()