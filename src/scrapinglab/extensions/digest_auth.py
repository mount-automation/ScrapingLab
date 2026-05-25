import asyncio
from playwright.async_api import (
    Page,
    Locator,
)
from .base_extension import BaseExtension

class DigestAuth(BaseExtension):
    url = 'https://the-internet.herokuapp.com/digest_auth'

    def get_context_options(self) -> dict[str, dict[str, str]]:
        return {
            'http_credentials': {
                'username': 'admin',
                'password': 'admin',
            },
        }

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        text: Locator = page.get_by_text(
            'Congratulations! You must have the proper credentials.'
        )
        await text.wait_for()
        if await text.is_visible():
            self.logger.info('DigestAuth module completed...')
            await asyncio.sleep(1.5)