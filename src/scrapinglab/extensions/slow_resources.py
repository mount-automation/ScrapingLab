from .core import BaseExtension
from playwright.async_api import (
    Page,
    Response,
)

class SlowResources(BaseExtension):
    url = 'https://the-internet.herokuapp.com/slow'

    async def run(self, page: Page) -> None:
        async with (
            page.expect_response(
                '**/slow_external', timeout=60000
            ) as response_info 
        ):
            await page.goto(self.url)
        request: Response = await response_info.value
        self.logger.info(request.url)
