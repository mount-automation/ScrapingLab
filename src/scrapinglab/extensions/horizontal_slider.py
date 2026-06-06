from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
import asyncio

class HorizontalSlider(BaseExtension):
    curr_value = 0
    url = 'https://the-internet.herokuapp.com/horizontal_slider'

    async def run(self, page: Page):
        await page.goto(self.url)
        await self._drag_slider(page=page, new_value=4)
        await self._drag_slider(page=page, new_value=4)
        await self._drag_slider(page=page, new_value=2)
        await asyncio.sleep(1.5)
    
    async def _drag_slider(self, page: Page, new_value: float):
        if new_value != self.curr_value:
            self.logger.info(
                f'Changing current slider value: '
                f'"{self.curr_value}" to "{new_value}"...')

            key_direction = ''

            if new_value > self.curr_value:
                key_direction = 'ArrowRight'
            elif new_value < self.curr_value:
                key_direction = 'ArrowLeft'

            steps: float = new_value / 0.5
            slider: Locator = page.get_by_role("slider")
            await slider.focus()
            for _ in range(int(steps)):
                await slider.press(key=key_direction)

            value: str = await page.locator('span#range').inner_text()
            self.curr_value = float(value.strip())

            self.logger.info(f'New slider value: "{self.curr_value}".')

        else:
            self.logger.info(
                'No change in slider value. Skipping slider operation...')