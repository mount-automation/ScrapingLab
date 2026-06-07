from ..core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Download,
)
from pathlib import Path
from typing import Literal

TARGET_LIST = Literal['PDF', 'CSV', 'Excel']

class JQueryUIMenu(BaseExtension):
    url = 'https://the-internet.herokuapp.com/jqueryui/menu'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        enable: Locator = page.get_by_role("link", name="Enabled")
        await self._download_something(link=enable, target='PDF')
        await self._return_to_ui(link=enable)

    async def _return_to_ui(self, link: Locator) -> None:
        page = link.page
        await link.hover()
        self.logger.info('Returning back to JQuery UI...')
        await page.get_by_role('link', name='Back to JQuery UI').click()
        ui_heading: Locator = page.get_by_role(
            'heading', level=3, name='JQuery UI')
        await ui_heading.wait_for(state='visible')
        if await ui_heading.is_visible():
            self.logger.info('Now at JQuery UI.')
        await self._return_to_menu(page=page)

    async def _return_to_menu(self, page: Page) -> None:
        self.logger.info('Returning back to JQueryUI Menu...')
        link_menu: Locator = page.get_by_role('link', name='Menu')
        await link_menu.click()
        menu_heading: Locator = page.get_by_role(
            'heading', level=3, name='JQueryUI - Menu')
        await menu_heading.wait_for(state='visible')
        if await menu_heading.is_visible():
            self.logger.info('Now at JQuery UI Menu page.')

    async def _download_something(
        self,
        link: Locator,
        target: TARGET_LIST) -> None:
        page: Page = link.page
        await link.hover()
        download_link: Locator = page.get_by_role("link", name="Downloads")
        await download_link.wait_for(state='visible')
        await download_link.hover()
        self.logger.info(f'Downloading {target}')
        async with (
            page.expect_download() as download_info
        ):
            await page.get_by_role('link', name=target).click()
        download: Download = await download_info.value
        save_place: Path = Path(__file__).resolve().parent
        save_place = save_place/download.suggested_filename
        await download.save_as(f'{save_place}')
        self.logger.info(f'File downloaded: {save_place}')


        