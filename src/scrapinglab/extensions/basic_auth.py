import asyncio
import logging
import json
from logging import Logger
from playwright.async_api import (
    Page,
    Browser,
    BrowserContext,
)

class BasicAuth:
    def __init__(self, browser: Browser|None = None) -> None:
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.url: str = ('https://the-internet.herokuapp.com/basic_auth')
        self.browser = browser
    
    async def init_extension(self) -> None:
        context: BrowserContext
        page: Page
        creds: dict[str, str] = {
            'username': 'admin',
            'password': 'admin',
        }
        self.logger.info(f'Attempting basic auth section: {self.url}')
        async with (
            await self.browser.new_context(
                http_credentials=creds
            ) as context,
            await context.new_page() as page,
        ):
            await page.goto(self.url)
            text = page.get_by_role('heading', name='Basic Auth')
            await text.wait_for()
            if await text.is_visible():
                self.logger.info(
                    f'Basic auth section passed with: '
                    f'{creds}...'
                )