from playwright.async_api import (
    Page,
    Locator,
    Response,
)
from ..core import BaseExtension
import random
import asyncio
import csv
from pathlib import Path

class FortiBleedScraper(BaseExtension):
    url = 'https://www.hudsonrock.com/fortinet'

    async def run(self, page: Page) -> None:
        all_results = []
        try:
            for i in range(601, 701):
                response: Response|None = await page.goto(
                    url=f'{self.url}?page={i}')
                await page.wait_for_load_state('domcontentloaded')
                if response is not None:
                    self.logger.info(f"Page {i} status: {response.status}")
                else:
                    raise ValueError('Response is None!')
                if response.status in (403, 429):
                    self.logger.warning(
                        f"Blocked/rate limited at page {i}. Stopping.")
                    break
                if i == 601:
                    await self.handle_cookie_popup(page=page)
                domain_list: list[tuple[str, str]] = await self.\
                    get_domain_surface_info(page=page)
                all_results.extend(domain_list)
                delay = random.uniform(3, 8)
                self.logger.info(f"Sleeping {delay:.2f} seconds")
                await asyncio.sleep(delay=delay)
        finally: 
            save_path = Path(__file__).resolve().parent
            save_path = save_path/'fortibleed_malaysia_domains.csv'
            with open(
                save_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as f:
                writer = csv.writer(f)
                writer.writerow(["domain", "sector"])
                writer.writerows(all_results)
            self.logger.info(
                f"Saved {len(all_results)} "
                f"results to fortibleed_malaysia_domains.csv"
            )

    async def get_domain_surface_info(
        self, page: Page) -> list[tuple[str, str]]:
        div: Locator = page.locator('div.space-y-4')
        await div.locator('article').first.wait_for(timeout=10000)
        article_list: list[Locator] = await div.locator('article').all()
        affected_domain_list = []
        for article in article_list:
            domain_url = await self.get_domain_url(article=article)
            if not domain_url.endswith('.my'):
                continue
            self.logger.info(f'Malaysian domain found: {domain_url}')
            sector = await self.get_sector(article=article)
            affected_domain_list.append((domain_url, sector))
        return affected_domain_list

    async def get_sector(self, article: Locator) -> str:
        sector_span: Locator = article.locator(
            r'div.hidden.sm\:flex.gap-4 '
            r'div.flex-1.min-w-0.flex.flex-col.gap-1 '
            r'div.flex.flex-wrap.items-center.gap-1\.5 '
            r'span span'
        ).first
        sector: str = (await sector_span.inner_text()).strip()
        if sector == '':
            raise ValueError('Sector string is empty!')
        return sector

    async def get_domain_url(self, article: Locator) -> str:
        h3: Locator = article.locator(
            r'div.hidden.sm\:flex.gap-4 '
            r'div.flex-1.min-w-0.flex.flex-col.gap-1 '
            r'div.flex.items-center.justify-between.gap-2 '
            r'div.flex.items-center.gap-2.min-w-0.flex-wrap '
            r'h3'
        )
        domain_url: str = (await h3.inner_text()).strip()
        if domain_url == '':
            raise ValueError('Domain url string is empty!')
        return domain_url

    async def handle_cookie_popup(self, page: Page) -> None:
        close_cookie_popup: Locator = page.get_by_role(
            "button", name="Reject All")
        if await close_cookie_popup.is_visible():
            await close_cookie_popup.click()
            self.logger.info('Cookie popup successfully closed.')
        else:
            self.logger.info('Cookie popup not found.')