from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

menu_choice: list[str] = ['Home', 'News', 'Contact', 'About']

class FloatingMenu(BaseExtension):
    url = 'https://the-internet.herokuapp.com/floating_menu'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        for i in range(1, 6):
            menu: Locator = page.locator('div#menu')
            before: bool = await menu.is_visible()

            await page.mouse.wheel(0, 1000)

            menu: Locator = page.locator('div#menu')
            after: bool = await menu.is_visible()
            await self._click_floating_menu(menu=menu)

            if before == after:
                self.logger.info(
                    f'Turn {i}: Menu visible after scrolling.')
            else:
                self.logger.info(
                    f'Turn {i}: Menu not visible after scrolling.')

    async def _click_floating_menu(
        self,
        menu: Locator,) -> None:
        for choice in menu_choice:
            target: Locator = menu.get_by_role('link', name=f'{choice}')
            await target.click()
            self.logger.info(target.page.url)
        