from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Dialog,
)
from typing import Literal

ACTION = Literal['accept', 'dismiss']

class JSAlerts(BaseExtension):
    url = 'https://the-internet.herokuapp.com/javascript_alerts'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._js_alert(page=page)
        await self._js_confirm(page=page)
        await self._js_prompt(page=page)

    async def _js_prompt(self, page: Page) -> None:
        prompt_button: Locator = page.get_by_role(
            'button', name='Click for JS Prompt')
        page.once('dialog', lambda dialog: self._dialog_handler(
            dialog=dialog, text='JS PROMPT!!!', action='accept'))
        await prompt_button.click()
        result: str = await page.locator('p#result').inner_text()
        self.logger.info(f'{result}')

    async def _js_confirm(self, page: Page) -> None:
        confirm_button: Locator = page.get_by_role(
            'button', name='Click for JS Confirm')
        page.once('dialog', lambda dialog: self._dialog_handler(
            dialog=dialog, text='', action='dismiss'))
        self.logger.info('Click JS confirm button.')
        await confirm_button.click()
        result: str = await page.locator('p#result').inner_text()
        self.logger.info(f'{result}')

    async def _js_alert(self, page: Page) -> None:
        alert_button: Locator = page.get_by_role(
            'button', name='Click for JS Alert')
        page.once('dialog', lambda dialog: self._dialog_handler(
            dialog=dialog, text='', action='accept'))
        self.logger.info('Click JS alert button.')
        await alert_button.click()
    
    async def _dialog_handler(
        self,
        dialog: Dialog,
        text: str,
        action: ACTION) -> None:
        message: str = dialog.message
        type: str = dialog.type
        self.logger.info(
            f'JS event of type "{type}" invoked.'
            f' Message: "{message}"')
        if action == 'accept':
            await dialog.accept(text)
            self.logger.info(f'"{type}" type event accepted.')
        elif action == 'dismiss':
            await dialog.dismiss()
            self.logger.info(f'"{type}" type event cancelled.')
        