from playwright.async_api import (
    Page,
    Locator,
    FrameLocator
)
from .base_frame import BaseFrame

class IFrame(BaseFrame):
    async def run_iframe(self) -> None:
        await self.click_frame_link(name='iFrame')
        
        