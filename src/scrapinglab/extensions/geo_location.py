from typing import Any

from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

class GeoLocation(BaseExtension):
    url = 'https://the-internet.herokuapp.com/geolocation'
    
    def get_context_options(self) -> dict[str, Any]:
        return {
            'permissions': ['geolocation'],
            'geolocation': {
                "latitude": 41.890221,
                "longitude": 12.492348
            }, # Rome, Italy
        }
    
    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        button: Locator = page.get_by_role('button', name='Where am I?')
        await button.click()
        latitude: str = await page.locator('div#lat-value').inner_text()
        longitude: str = await page.locator('div#long-value').inner_text()
        await page.get_by_role('link', name='See it on Google').click()
        location: str = await page.locator('span.DkEaL').nth(0).inner_text()
        self.logger.info(f'Latitude: {latitude}')
        self.logger.info(f'Longitude: {longitude}')
        self.logger.info(f'Location (Google Map): {location}')