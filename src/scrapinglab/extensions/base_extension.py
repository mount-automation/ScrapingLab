import logging
from typing import ClassVar, Any
from logging import Logger
from abc import ABC, abstractmethod
from playwright.async_api import (
    Page,
    Browser,
    BrowserContext,
)

class BaseExtension(ABC):
    url: ClassVar[str]

    def __init__(self, browser: Browser) -> None:
        self.browser: Browser = browser
        self.logger: Logger = logging.getLogger(self.__class__.__name__)

    def get_context_options(self) -> dict[str, Any]:
        return {}

    async def init_extension(self) -> None:
        page: Page
        context: BrowserContext
        async with(
            await self.browser.new_context(
                **self.get_context_options()
            ) as context,
            await context.new_page() as page,
        ):
            await self.run(page=page)

    @abstractmethod
    async def run(self, page: Page) -> None:
        pass
