import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Locator,
)

class BaseFrame:
    page: Page
    logger: Logger

    def __init__(self, page: Page, logger: Logger) -> None:
        self.page = page
        self.logger = logging.getLogger(
            f'{logger.name}.{self.__class__.__name__}')
        
    async def click_frame_link(self, name: str):
        link: Locator = self.page.get_by_role('link', name=name)
        await link.click()