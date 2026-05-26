import random
import asyncio
from oxymouse import OxyMouse
from .core import BaseExtension
from playwright.async_api import (
    Page,
    Browser,
    Locator,
)

class DragAndDrop(BaseExtension):
    url = 'https://the-internet.herokuapp.com/drag_and_drop'

    def __init__(self, browser: Browser) -> None:
        super().__init__(browser=browser)
        self.debug_timeout = 3 

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        col_a: Locator = page.locator('#column-a')
        col_b: Locator = page.locator('#column-b')
        # await self._simple_drag(locator_src=col_a, locator_dst=col_b)
        await self._human_emulation(locator_src=col_a, locator_dst=col_b)
        self.logger.info('DragAndDrop module test done')
    
    async def _get_box_status(
        self, **kwargs: Locator
    ) -> list[tuple[str, str]]:
        column: Locator
        box_status_dict = dict()
        for _, column in kwargs.items():
            column_id: str = await column.get_attribute('id')
            text: str = await column.inner_text()
            box_status_dict[column_id] = text
        return box_status_dict

    async def _human_emulation(
        self, locator_src: Locator, locator_dst: Locator
    ) -> None:
        page = locator_src.page
        await self._add_debug_cursor(page=page)
        box_src = await locator_src.bounding_box()
        box_dst = await locator_dst.bounding_box()

        src_centre_x = box_src['x'] + (
            box_src['width'] * random.uniform(0.3, 0.7))
        src_centre_y = box_src['y'] + (
            box_src['height'] * random.uniform(0.3, 0.7))
        dst_centre_x = box_dst['x'] + (
            box_dst['width'] * random.uniform(0.3, 0.7))
        dst_centre_y = box_dst['y'] + (
            box_dst['height'] * random.uniform(0.3, 0.7))
        
        mouse = OxyMouse(algorithm='bezier')
        movements = mouse.generate_coordinates(
            from_x=int(src_centre_x), 
            from_y=int(src_centre_y), 
            to_x=int(dst_centre_x), 
            to_y=int(dst_centre_y),)
        
        before: list[tuple[str, str]] = await self._get_box_status(
            locator_src=locator_src, locator_dst=locator_dst)
        self.logger.info('Starting human behaviour emulation.')
        for i, (x, y) in enumerate(movements, start=1):
            x = int(x)
            y = int(y)
            await page.mouse.move(x, y)
            await page.evaluate("""
                ([x, y]) => {
                    const c = document.getElementById('debug-cursor');
                    c.style.left = `${x}px`;
                    c.style.top = `${y}px`;
                }
            """, [x, y])
            if i == 1:
                await page.mouse.down()
            await asyncio.sleep(random.uniform(0.02, 0.03))
        await page.mouse.up()
        after: list[tuple[str, str]] = await self._get_box_status(
            locator_src=locator_src, locator_dst=locator_dst)
        success: bool = (
            before['column-a'] != after['column-a']
            and 
            before['column-b'] != after['column-b']
        )
        if success:
            self.logger.info('Box swapping succedded.')
        else:
            self.logger.info('Box swapping failed.')

    async def _add_debug_cursor(self, page: Page):
        await page.evaluate("""
        () => {
            const cursor = document.createElement('div');
            cursor.id = 'debug-cursor';
            cursor.style.cssText = `
                position: fixed;
                width: 14px;
                height: 14px;
                background: red;
                border: 2px solid white;
                border-radius: 50%;
                z-index: 999999;
                pointer-events: none;
                left: 0px;
                top: 0px;
            `;
            document.body.appendChild(cursor);
        }
        """)

    async def _simple_drag(
        self, locator_src: Locator, locator_dst: Locator
    ) -> None:
        await locator_src.drag_to(locator_dst)
        self.logger.info('Simple drag and drop action executed')
        await asyncio.sleep(self.debug_timeout)