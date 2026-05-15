import asyncio
from playwright.async_api import async_playwright

class Extension1:
    def __init__(self, browser=None):
        self.browser = browser
        self.url = 'https://the-internet.herokuapp.com/abtest'

    async def init_extension(self):
        async with (
            await self.browser.new_context() as context, 
            await context.new_page() as page,
        ):
            await page.goto(self.url)
            div = page.locator('div.example')
            header = div.get_by_role('heading', level=3)

            await header.wait_for()

            header_text = await header.inner_text()
        self._confirm_result(url=self.url, text=header_text)
        await asyncio.sleep(5)
        print(f'{self.__class__.__name__} is done...\n')

    @staticmethod
    def _confirm_result(url='', text=''):
        header_text_list = ['A/B Test Variation 1', 'A/B Test Control']
        if text in header_text_list:
            print(f'Current header is "{text}" in "{url}"...')
        else:
            print(f'"{text}" not found in records...')