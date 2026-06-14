from typing import Any
from playwright.async_api import (
    Page,
)
from .core import BaseExtension

class BasicAuth(BaseExtension):
    url = 'https://the-internet.herokuapp.com/basic_auth'
    creds = {
            'http_credentials': {
                'username': 'admin',
                'password': 'admin',
            },
        } 
    
    def get_context_options(self) -> dict[str, Any]:
        return self.creds

    async def run(self, page: Page) -> None:
        self.logger.info(f'Attempting basic auth section: {self.url}')
        await page.goto(self.url)
        text = page.get_by_role('heading', name='Basic Auth')
        await text.wait_for()
        if await text.is_visible():
            self.logger.info(
                f'Basic auth section passed with: '
                f'{self.creds}...'
            )