from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Response,
)

class StatusCodes(BaseExtension):
    url = 'https://the-internet.herokuapp.com/status_codes'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        link_list: list[Locator] = await page.get_by_role('link').all()
        for link in link_list:
            text: str = await link.inner_text()
            try:
                number: float = float(text.strip())
            except ValueError:
                continue
            async with(
                page.expect_response(f'**/{int(number)}') as response_info
            ):
                await link.click()
            response: Response = await response_info.value
            code: int = response.status
            self.logger.info(f'Response caught. Status code: {code}')
            await page.goto(self.url)