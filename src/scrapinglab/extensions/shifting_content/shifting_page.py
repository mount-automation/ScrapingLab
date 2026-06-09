import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Locator,
)

class ShiftingPage:
    link: Locator
    logger: Logger
    home_url: str

    def __init__(
        self,
        home_url: str,
        link: Locator,
        logger: Logger) -> None:
        self.home_url = home_url
        self.link = link
        self.logger = logging.getLogger(
            f'{logger.name}.{self.__class__.__name__}')
    
    async def init_page(self) -> Page:
        page: Page = self.link.page
        await self.link.click()
        return page