from ..core import BaseExtension
from .nested_frames import NestedFrames
from .iframe import IFrame
from playwright.async_api import (
    Page,
)

class FrameHandler(BaseExtension):
    url = 'https://the-internet.herokuapp.com/frames'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        nested_frame_handler: NestedFrames = NestedFrames(
            page=page, logger=self.logger)
        await nested_frame_handler.run_nested_frames()
        await page.go_back()
        iframe_handler: IFrame = IFrame(page=page, logger=self.logger)
        await iframe_handler.run_iframe()
        





        
