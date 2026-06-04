from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Response,
)

class ForgotPassword(BaseExtension):
    url = 'https://the-internet.herokuapp.com/forgot_password'

    async def run(self, page: Page) -> None:
        await page.goto(self.url, timeout=60000)
        textbox: Locator = page.get_by_role('textbox', name='E-mail')
        await textbox.focus()
        text = 'whatever324@gmail.com'
        await textbox.press_sequentially(text=text, delay=50)
        button: Locator = page.get_by_role('button', name='Retrieve password')
        await button.hover()
        expected_url = 'https://the-internet.herokuapp.com/forgot_password'
        async with (
            page.expect_response(expected_url) as response_info
        ):
            await button.click()
        response: Response = await response_info.value
        if response.status > 399:
            self.logger.info('Password retrieval failed.')
        else:
            self.logger.info('Password retrieval succeeded.')
        