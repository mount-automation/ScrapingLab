import logging
from logging import Logger
from playwright.async_api import (
    Page,
    Locator,
    FrameLocator
)
from .base_frame import BaseFrame

class NestedFrames(BaseFrame):
    async def run_nested_frames(self) -> None:
        await self.click_frame_link(name='Nested Frames')
        main_frameset: Locator = self.page.locator('frameset')
        await self._handle_top_frame(main_frameset=main_frameset)
        await self._handle_bottom_frame(main_frameset=main_frameset)

    async def _handle_bottom_frame(self, main_frameset: Locator) -> None:
        bottom_frame: FrameLocator = main_frameset.frame_locator(
            f'frame[name="frame-bottom"]')
        page: FrameLocator = bottom_frame
        text: str = await page.locator('body').inner_text()
        self._log_info(text=text)

    async def _handle_top_frame(self, main_frameset: Locator) -> None:
        top_frame: FrameLocator = main_frameset.frame_locator(
            f'frame[name="frame-top"]')
        frame_list: list[Locator] = await top_frame.locator(
            'frameset').locator('frame').all()
        for frame in frame_list:
            frame_name: str|None = await frame.get_attribute('name')
            frame_content: FrameLocator = frame.content_frame
            if frame_name is not None:
                await self._handle_frame_content(
                    frame_name=frame_name, frame_content=frame_content)
            else:
                raise ValueError('Frame specified name not found.')

    async def _handle_frame_content(
        self, frame_name: str,
        frame_content: FrameLocator) -> None:
        page = frame_content
        if 'left' in frame_name:
            text: str = await page.locator('body').inner_text()
            self._log_info(text=text)
        elif 'middle' in frame_name:
            text: str = await page.locator('div#content').inner_text()
            self._log_info(text=text)
        elif 'right' in frame_name:
            text: str = await page.locator('body').inner_text()
            self._log_info(text=text)
            
    def _log_info(self, text: str) -> None:
        self.logger.info(f'{text} frame detected. Message: "{text}"')