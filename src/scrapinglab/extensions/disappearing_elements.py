import asyncio
from playwright.async_api import (
    Page,
    Locator,
)
from .base_extension import BaseExtension

class DisappearingElements(BaseExtension):
    url = 'https://the-internet.herokuapp.com/disappearing_elements'

    async def run(self, page: Page) -> None:
        task_not_done = True
        while task_not_done:
            await page.goto(self.url)
            div: Locator = page.locator('div.example')
            ul: Locator = div.locator('ul').filter(
                has=page.locator('li')
            )
            li_list: list[Locator] = await ul.locator('li').all()
            for i, li in enumerate(li_list):
                if await li.inner_text() == 'Gallery':
                    self.logger.info('Gallery link found. Clicking it...')
                    await self._click_verify_button(li)
                    task_not_done = False
                    await asyncio.sleep(1.5)
                    break
                elif i == len(li_list) - 1:
                    self.logger.info('Gallery link not found. Reloading page...')
                    await asyncio.sleep(1.5)
        self.logger.info(f'Dissapearing Elements module test done...')

    async def _click_verify_button(self, element: Locator) -> None:
        async with (
            element.page.expect_response(
                'https://the-internet.herokuapp.com/gallery/'
            ) as hook_response
        ):
            await element.click()
        value = await hook_response.value
        self.logger.info(f'Link clicked. New URL is {value.url}...')