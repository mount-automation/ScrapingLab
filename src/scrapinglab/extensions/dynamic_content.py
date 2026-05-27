import asyncio
from .core import BaseExtension
from typing import Literal
from playwright.async_api import (
    Page,
    Browser,
    Locator,
)

class DynamicContent(BaseExtension):
    url = 'https://the-internet.herokuapp.com/dynamic_content'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        div: Locator = page.locator('div.example')
        div: Locator = div.locator('div.row')
        div: Locator = div.locator('div#content')
        div_row_list: list[Locator] = await div.locator('div.row').all()

        self.logger.info('Saving before state...')
        before: list[dict[str, str]] = list()
        for div_row in div_row_list:
            row: dict[str, str] = await self._parse_row(div_row=div_row)
            before.append(row)

        self.logger.info('Reloading page...')
        await page.goto(self.url)

        self.logger.info('Saving after state...')
        after: list[dict[str, str]] = list()
        for div_row in div_row_list:
            row: dict[str, str] = await self._parse_row(div_row=div_row)
            after.append(row)       
        
        self.logger.info('Comparing state...')
        for i in range(len(before)):
            changed = (
                before[i]['image'] != after[i]['image']
                or
                before[i]['text'] != after[i]['text']
            )
            if changed:
                self.logger.info(f'Row {i} have changed!')


    async def _parse_row(self, div_row: Locator) -> dict[str, str]:
        img: Locator = div_row.get_by_role('img')
        image: str = await img.get_attribute('src')
        text: str = await div_row.inner_text()
        row: dict[str, str] = dict(image=image, text=text)
        return row
