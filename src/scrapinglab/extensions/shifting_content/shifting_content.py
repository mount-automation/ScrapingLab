from ..core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)
from .shifting_menu import ShiftingMenu
from .shifting_image import ShiftingImage

class ShiftingContent(BaseExtension):
    url = 'https://the-internet.herokuapp.com/shifting_content'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        link_list: list[Locator] = await page.get_by_role('link').all()
        for link in link_list:
            name: str = await link.inner_text()
            if 'Example 1' in name:
                menu: ShiftingMenu = ShiftingMenu(
                    home_url=self.url, link=link, logger=self.logger)
                await menu.proceed()
            elif 'Example 2' in name:
                image: ShiftingImage = ShiftingImage(
                    home_url=self.url, link=link, logger=self.logger)
                await image.proceed()