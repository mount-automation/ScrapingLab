from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Download,
)
import asyncio

class FileDownloader(BaseExtension):
    url = 'https://the-internet.herokuapp.com/download'

    async def run(self, page: Page) -> None:
        await page.goto(self.url, timeout=60000)
        div: Locator = page.locator('div.example')
        link_list: list[Locator] = await div.get_by_role('link').all()
        for link in link_list:
            filename: str = await link.inner_text()
            if '.txt' in filename:
                await self._download_file(link=link)
                
    async def _download_file(self, link: Locator):
        async with(
            link.page.expect_download() as download_info
        ):
            await link.click()
        download: Download = await download_info.value
        await download.save_as(
            f"C:\\Users\\MaeganMaulder\\Downloads\\TEST\\"
            f"{download.suggested_filename}")
        self.logger.info(f'Downloaded {download.suggested_filename}')