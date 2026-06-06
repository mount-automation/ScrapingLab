import re
from re import Match
from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

class Hovers(BaseExtension):
    url = 'https://the-internet.herokuapp.com/hovers'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        div: Locator = page.locator('div.example')
        img_list: list[Locator] = await div.get_by_role('img').all()
        for img in img_list:
            await self._hover_over_image(img=img)


    async def _hover_over_image(self, img: Locator) -> None:
        page: Page = img.page
        await img.hover()

        profile_list: list[Locator] = await page.get_by_text('name:').all()
        for profile in profile_list:
            found: bool = await self._parse_profile(profile=profile)
            if found:
                break

        link_list: list[Locator] = await page.get_by_role(
            'link', name='View profile').all()
        for link in link_list:
            found: bool = await self._navigate_link(link=link)
            if found:
                await page.go_back()
                break
            await page.go_back()


    async def _navigate_link(self, link: Locator) -> bool:
        if await link.is_visible():
            page: Page = link.page
            response_url = re.compile(
                r'https://the-internet\.herokuapp\.com/users/[0-9]+')
            async with (
                page.expect_response(response_url) as response_info
            ):
                await link.click()
            response = await response_info.value
            if response.status > 399:
                self.logger.info(f'"{response.url}" not working as expected.')
            else:
                self.logger.warning(
                    f'"{response.url}" returns status lesser than 400.'
                    f' This should not have happened.')
            return True
        return False
            

    async def _parse_profile(self, profile: Locator) -> bool:
        if await profile.is_visible():
            text: str = await profile.inner_text()
            searched: Match[str]|None = re.search(
                r'name: ([a-zA-Z0-9]+)', text)
            if searched:
                user_name: str = searched.group(1)
            else:
                raise ValueError('Failed to extract name via regex.')
            self.logger.info(
                f'Hovered over "{user_name}".')
            return True
        return False