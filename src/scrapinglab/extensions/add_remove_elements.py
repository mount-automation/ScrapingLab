import asyncio
from playwright.async_api import (
    Browser,
    Page,
    Locator,
)
from .base_extension import BaseExtension

class AddRemoveElements(BaseExtension):
    url = 'https://the-internet.herokuapp.com/add_remove_elements/'

    def __init__(self, browser: Browser) -> None:
        super().__init__(browser=browser)
        self._amnt_elements = 0
    
    async def run(self, page: Page) -> None:
        self.page = page
        await self.page.goto(self.url)
        await self._entry_point()

    async def _entry_point(self) -> None:
        try:
            self._amnt_elements = await self._confirm_element_amount()
            if self._amnt_elements > 0:
                self.logger.info(
                    f'{self._amnt_elements} '
                    'element(s) will be added into queue...'   
                )
                await self._add_element(
                    page=self.page, amount=self._amnt_elements
                )
                await self._delete_element(
                    page=self.page, amount=self._amnt_elements
                )

            else:
                self.logger.info(
                    'No elements to be added into work queue: '
                    f'{self._amnt_elements} element(s)'
                )
        except Exception:
            self.logger.exception(f'Something went wrong: ')

    async def _confirm_element_amount(self) -> int:
        while True:
            user_input: str = await asyncio.to_thread(
                input, 'Amount of elements to add: '
            )
            try:
                user_input = int(user_input)
                if user_input < 0:
                    self.logger.warning('Input must be >= 0')
                    continue
            except ValueError:
                self.logger.error(
                    'Input must be integers only e.g. 5. Try again.'
                )
            else:
                break
        return user_input

    async def _add_element(
        self, page: Page|None = None, amount: int = 0
    ) -> None:
        if amount > 0:
            self.logger.info(
                f'Adding {amount} element(s) into queue...'
            )
        add_button: Locator = page.get_by_role(
            'button', name='Add Element'
        )
        for _ in range(amount):
            await add_button.click()
            await asyncio.sleep(1)

    async def _delete_element(
        self, page: Page|None = None, amount: int = 0
    ) -> None:
        div_example: Locator = page.locator('div.example')
        div_elements: Locator = div_example.locator('div#elements')
        delete_button: Locator = div_elements.get_by_role(
            'button', name='Delete'
        ).first
        for _ in range(amount):
            await delete_button.click()
            await asyncio.sleep(1)
        self.logger.info(f'{amount} button(s) deleted...')
