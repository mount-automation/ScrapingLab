import asyncio
from playwright.async_api import (
    Page,
    Locator,
)
from .core import BaseExtension

class CheckBoxes(BaseExtension):
    url = 'https://the-internet.herokuapp.com/checkboxes' 
    
    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        if await self._click_checkbox(page=page):
            self.logger.info('Checkbox stage done...')

    async def _click_checkbox(self, page: Page) -> bool:
        checkbox_list: list[Locator] = await page.get_by_role(
            'checkbox').all()
        for id, checkbox in enumerate(checkbox_list, start=1):
            status_ticked: bool = await checkbox.is_checked()
            if status_ticked:
                self.logger.info(f'Checkbox{id} is checked, '
                    'proceed to uncheck it...')
                await checkbox.set_checked(not status_ticked)
            else:
                self.logger.info(f'Checkbox{id} is unchecked, '
                    'proceed to check it...')
                await checkbox.set_checked(not status_ticked)
            await asyncio.sleep(1.5)
        return True

