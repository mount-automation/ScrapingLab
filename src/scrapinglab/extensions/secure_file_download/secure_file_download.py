from typing import Any
from ..core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Download,
)
from pathlib import Path

class SecureFileDownload(BaseExtension):
    url = 'https://the-internet.herokuapp.com/download_secure'

    def get_context_options(self) -> dict[str, Any]:
        return {
            'http_credentials': {
                'username': 'admin',
                'password': 'admin',
            },
        }
    
    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        link_list: list[Locator] = await page.get_by_role('link').all()
        for link in link_list:
            name: str = await link.inner_text()
            if name != '':
                async with(
                    page.expect_download() as download_info 
                ):
                    await link.click()
                download: Download = await download_info.value
                save_place: Path = Path(__file__).resolve().parent
                save_place: Path = save_place/download.suggested_filename
                await download.save_as(save_place)
                self.logger.info(f'Downloaded: {save_place}')
                break