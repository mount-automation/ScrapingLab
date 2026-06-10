from playwright.async_api import (
    Page,
    Locator,
    FloatRect,
)
from .shifting_page import ShiftingPage

class ShiftingImage(ShiftingPage):
    async def proceed(self) -> None:
        page: Page = await self.init_page()
        link_list: list[Locator] = await page.get_by_role(
            'link', name='click here').all()
        for link in link_list:
            mode_url: str|None = await link.get_attribute('href')
            if not mode_url:
                raise ValueError('Mode url not found.')
            if 'mode=random' in mode_url and 'pixel_shift' in mode_url:
                await page.locator('img.shift').wait_for(state='visible')
                image_scale_before: FloatRect|None = await page.locator(
                    'img.shift').bounding_box()
                await link.click()
                await page.wait_for_load_state('domcontentloaded')
                image_scale_after: FloatRect|None = await page.locator(
                    'img.shift').bounding_box()
                if image_scale_before and image_scale_after:
                    status = (
                        image_scale_before['y'] == image_scale_after['y']
                        and 
                        image_scale_before['x'] != image_scale_after['x']
                    )
                    if status:
                        self.logger.info(
                            'Image successfully captured '
                            'and its position shifted.')
                        await page.goto(self.home_url)
                        break
                    else:
                        self.logger.info(
                            'Something went wrong during' \
                            ' the image scale checking.')
                        self.logger.info(f'{image_scale_before}')
                        self.logger.info(f'{image_scale_after}')
                        raise ValueError(
                            'Something went wrong during ' \
                            'the image scale checking.')