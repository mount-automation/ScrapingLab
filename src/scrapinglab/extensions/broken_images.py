import asyncio
import logging
from logging import Logger
from urllib.parse import urljoin
from playwright.async_api import (
    Page,
    Browser,
    Locator,
    BrowserContext,
    APIResponse
)

class BrokenImages:
    def __init__(self, browser: Browser|None = None) -> None:
        self.url: str = ('https://the-internet.herokuapp.com/broken_images')
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.browser: Browser = browser
    
    async def init_extension(self) -> None:
        context: BrowserContext
        page: Page
        async with (
            await self.browser.new_context() as context,
            await context.new_page() as page,
        ):
            await page.goto(self.url)
            await self._entry_point(page=page)

    async def _entry_point(
        self, page: Page|None = None
    ) -> None:
        result: tuple[bool, list] = await self._compare_result(
            await self._check_dimension(page=page),
            await self._check_response(page=page),
        )
        if result[0]:
            broken_img_url: list[str] = result[1]
            self.logger.info(
                f'Found {len(broken_img_url)} broken images: {broken_img_url}'
            )
        else:
            self.logger.info(f'No broken images found...')
    
    async def _check_dimension(self, page: Page|None = None) -> list[str]:
        images: Locator = page.get_by_role('img')
        broken_img_url: list[str] = await images.evaluate_all('''
            images => images
                .filter(
                    image =>
                    image.naturalHeight === 0 &&
                    image.naturalWidth === 0 &&
                    image.complete
                )
                .map(image => image.src)
        ''')
        return broken_img_url
    
    async def _check_response(self, page: Page|None = None) -> list[str]:
        div: Locator = page.locator('div.example')
        div: Locator = div.filter(has=page.get_by_role('heading', level=3))
        img_list: list[Locator] = await div.get_by_role('img').all()
        broken_img_url: list[str] = []
        for img in img_list:
            img_url: str = await img.get_attribute('src')
            img_url = urljoin(page.url, img_url)
            response: APIResponse = await page.request.get(img_url)
            status_code: int = response.status
            if status_code >= 400:
                broken_img_url.append(img_url)
        return broken_img_url
    
    async def _compare_result(
        self, *results: list[str]
    ) -> tuple[bool, list[str]]:
        list_of_sets: list[set] = [set(res) for res in results]
        first_set: set = list_of_sets[0]
        check_result: bool = all(
            first_set == curr_set for curr_set in list_of_sets
        )
        if check_result:
            return (check_result, list(first_set))
        else:
            return (check_result, [])


        





