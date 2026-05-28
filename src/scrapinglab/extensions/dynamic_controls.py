import asyncio
from .core import BaseExtension
from typing import Literal
from playwright.async_api import (
    Page,
    Browser,
    Locator,
)

class DynamicControls(BaseExtension):
    url = 'https://the-internet.herokuapp.com/dynamic_controls'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._remove_checkbox(page=page)
        await self._add_checkbox(page=page)
        await self._enable_textbox(page=page)
        await self._disable_textbox(page=page)

    async def _disable_textbox(self, page: Page) -> None:
        button: Locator = page.get_by_role('button', name='disable')
        textbox: Locator = page.get_by_role('textbox')
        disabled: str|None = await textbox.get_attribute('disabled')
        if isinstance(disabled, type(None)):
            self.logger.info('Textbox enabled.')
            self.logger.info('Disabling textbox...')            
            await button.click()
            self.logger.info('Textbox disabled.')
        else:
            self.logger.warning('Textbox is already disabled!')
            raise ValueError('Textbox is already disabled!')

    async def _enable_textbox(self, page: Page) -> None:
        button: Locator = page.get_by_role('button', name='Enable')
        textbox: Locator = page.get_by_role('textbox')
        # The disabled attribute does not actually have a value but
        # by default, get_attribute() returns an empty string if the 
        # attribute does exist. 
        disabled: str|None = await textbox.get_attribute('disabled')
        if isinstance(disabled, str):
            self.logger.info('Textbox disabled.')
            self.logger.info('Enabling textbox...')
            await button.click()
            self.logger.info('Textbox enabled.')
            self.logger.info('Filling in textbox with texts...')
            await textbox.fill('This is a test.')
            self.logger.info('Textbox filled in.')
        else:
            self.logger.warning('Textbox is already enabled!')
            raise ValueError('Textbox is already enabled!')

    async def _remove_checkbox(self, page: Page) -> None:
        button: Locator = page.get_by_role('button', name='Remove')
        checkbox: Locator = page.get_by_role('checkbox')
        if await button.is_visible():
            self.logger.info('Removing checkbox...')
            await button.click()
            await checkbox.wait_for(state='hidden', timeout=5000)
            self.logger.info('Checkbox removed successfully.')

    async def _add_checkbox(self, page: Page) -> None:
        button: Locator = page.get_by_role('button', name='Add')
        checkbox: Locator = page.get_by_role('checkbox')
        if await button.is_visible():
            self.logger.info('Adding checkbox...')
            await button.click()
            await checkbox.wait_for(timeout=5000)
            self.logger.info('Checkbox added successfully.')
    


        
        