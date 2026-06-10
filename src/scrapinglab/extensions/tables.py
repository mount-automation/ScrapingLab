from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
)

class Tables(BaseExtension):
    url = 'https://the-internet.herokuapp.com/tables'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._parse_example_1(page=page)
        
    async def _parse_example_1(self, page: Page) -> None:
        table_1: Locator = page.locator('table#table1')
        headers: list[str] = await self._parse_header(table=table_1)
        records: list[dict] = await self._parse_body(table=table_1, headers=headers)
        for record in records: 
            self.logger.info(record)

    async def _parse_body(self, table: Locator, headers: list[str]) -> list[dict]:
        body_tr_list: list[Locator] = await table.locator(
            'tbody').locator('tr').all()
        full_record: list = []
        for body_tr in body_tr_list:
            body_td_list: list[Locator] = await body_tr.locator(
                'td').filter(has_not_text='edit').all()
            record: dict = {}
            for i, body_td in enumerate(body_td_list):
                info: str = await body_td.inner_text()
                record[headers[i]] = info
            full_record.append(record)
        return full_record
             
    async def _parse_header(self, table: Locator) -> list[str]:
        head_tr: Locator = table.locator('thead').locator('tr')
        head_th_list: list[Locator] = await head_tr.locator(
            'th.header').all()
        headers: list = []
        for head_th in head_th_list:
            text: str = await head_th.inner_text()
            if text == 'Action':
                break
            headers.append(text.strip())
        return headers