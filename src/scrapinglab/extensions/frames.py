from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    FrameLocator
)

class FrameHandler(BaseExtension):
    url = 'https://the-internet.herokuapp.com/frames'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._nested_frames(page=page)

    async def _nested_frames(self, page: Page) -> None:
        link: Locator = page.get_by_role('link', name='Nested Frames')
        await link.click()
        main_frameset: Locator = page.locator('frameset')
        frame_pos = 'top'
        await self._handle_base_frame(frame_pos=frame_pos, main_frameset=main_frameset)
        frame_pos = 'bottom'
        await self._handle_base_frame(frame_pos=frame_pos, main_frameset=main_frameset)

    async def _handle_base_frame(self, frame_pos: str, main_frameset: Locator) -> None:
        top_frame: FrameLocator = main_frameset.frame_locator(
            f'frame[name="frame-{frame_pos}"]')
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
        elif 'bottom' in frame_name:
            text: str = await page.locator('body').inner_text()
            self._log_info(text=text)
            
    def _log_info(self, text: str) -> None:
        self.logger.info(f'{text} frame detected. Message: "{text}"')



        
