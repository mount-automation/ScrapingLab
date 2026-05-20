import asyncio
import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Browser,
    BrowserContext,
)


class ChallengingDOM:
    def __init__(self, browser: Browser|None = None) -> None:
        self.browser = browser
        self.url = ''