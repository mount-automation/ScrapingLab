from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
import asyncio

class Inputs(BaseExtension):
    url = 'https://the-internet.herokuapp.com/inputs'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._set_value(page=page, amount=10)
        await asyncio.sleep(1)
        await self._set_value(page=page, amount=-5)

    async def _set_value(self, page: Page, amount: int) -> None:
        spinbutton: Locator = page.get_by_role("spinbutton")
        try:
            existing_input: int = int(await spinbutton.input_value())
        except ValueError:
            existing_input = 0
        key_direction = ''
        if amount == existing_input:
            self.logger.info(
                'Amount is the same as existing input. Operation skipped.')
            return
        elif amount > existing_input:
            key_direction = 'ArrowUp'
        elif amount < existing_input:
            key_direction = 'ArrowDown'
        self.logger.info('Setting input value till target amount reached...')
        while amount != existing_input:
            await spinbutton.press(key=key_direction)
            existing_input: int = int(await spinbutton.input_value())
        self.logger.info(f'Spinbutton input now reached {amount}')
