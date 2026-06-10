from playwright.async_api import (
    Page,
    Locator,
    FloatRect,
    FrameLocator,
)
from .core import BaseExtension

class TinyMCE(BaseExtension):
    url = 'https://the-internet.herokuapp.com/tinymce'

    async def run(self, page: Page) -> None:
        self.page: Page = page
        await page.goto(self.url)
        await self.run_iframe()

    async def run_iframe(self) -> None:
        close_button: Locator = self.page.get_by_role(
            "button", name="Close")
        await close_button.click()
        await self._resize_textbox(page=self.page)
        await self._try_textbox(page=self.page)
    
    async def _try_textbox(self, page: Page):
        textarea: Locator = page.locator('textarea')
        if await textarea.is_editable() and await textarea.is_visible():
            self.logger.info('Textbox is visible and editable.')
        else:
            self.logger.info(
                'Textbox is not editable, not visible or both.')
        iframe: FrameLocator = page.frame_locator('iframe')
        body_text: str = await iframe.locator('p').inner_text()
        self.logger.info(f'Message in textbox captured: {body_text}')

    async def _resize_textbox(self, page: Page):
        resize_dragger: Locator = page.locator(
            ".tox-statusbar__resize-handle > svg")
        box: FloatRect|None = \
            await resize_dragger.bounding_box()
        if box is not None:
            start_x: float = box['x'] + box['width'] / 2
            start_y: float = box['y'] + box['height'] / 2
        else:
            raise ValueError('Failed to acquire UI dimensions.')
        self.logger.info(f'Resizing textbox size...')        
        await resize_dragger.hover()
        await resize_dragger.page.mouse.down()
        await resize_dragger.page.mouse.move(
            x=start_x, y=start_y + 500, steps=10)
        await resize_dragger.page.mouse.up()
        self.logger.info('Resizing done...')