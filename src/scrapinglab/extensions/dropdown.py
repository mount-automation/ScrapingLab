import asyncio
from .core import BaseExtension
from typing import Literal
from playwright.async_api import (
    Page,
    Browser,
    Locator,
)

class Dropdown(BaseExtension):
    url = 'https://the-internet.herokuapp.com/dropdown'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        combobox: Locator = page.get_by_role('combobox')
        await self._click_option(combobox=combobox, choice='Option 1')
        await self._click_option(combobox=combobox, choice='Option 2')
        self.logger.info('Dropdown module challenge done')
    
    async def _click_option(
        self,
        combobox: Locator, 
        choice: Literal['Option 1', 'Option 2'],
    ) -> None:
        if choice not in ['Option 1', 'Option 2']:
            self.logger.error('Wrong choice!')
            raise ValueError
        self.logger.info(f'Clicking {choice}')
        await combobox.select_option(choice)
        selected = await combobox.input_value()
        if selected in choice:
            self.logger.info(f'{choice} had been selected')
        else:
            self.logger.info(f'{choice} had not been selected')
        await asyncio.sleep(1.5)
    
        
