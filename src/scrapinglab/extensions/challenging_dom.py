import re
import json
from re import Match
import asyncio
from playwright.async_api import (
    Page,
    Locator,
)
from .core import BaseExtension

type TableData = list[dict[str, str]]

class ChallengingDOM(BaseExtension):
    url = 'https://the-internet.herokuapp.com/challenging_dom'
    
    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        await self._entry_point(page=page)

    async def _entry_point(self, page: Page) -> None:
        status: bool = await self._click_buttons(page=page)
        if status:
            self.logger.info('First stage of the test done...')
        status: bool = await self._parse_table(page=page)
        if status:
            self.logger.info('Second stage of the test done...')
        status: bool = await self._press_edit_delete(page=page)
        if status:
            self.logger.info('Third stage of the test done...')

    async def _press_edit_delete(self, page: Page) -> bool:
        element_name_list: list[str] = ['edit', 'delete']
        for name in element_name_list:
            self.logger.info(
                f'Clicking {name} link on row 5 with 1.5 secs interval...'
            )
            await asyncio.sleep(1.5)
            link: Locator = page.get_by_role('link', name=f'{name}').nth(5)
            await link.click() 
        return True

    async def _parse_table(self, page: Page) -> bool:
        table: Locator = page.locator('table')
        column_header_list: list[str] = await self._parse_column_headers(
            page=page, table=table
        )
        tbody: Locator = table.locator('tbody')
        table_data_list: TableData = await self._parse_table_row(
            page=page,
            tbody=tbody, 
            column_headers=column_header_list,
        )
        if table_data_list:
            self.logger.info(f'Table Data extracted: '
                f'\n{json.dumps(table_data_list, indent=4)}')
            return True
        return False

    async def _parse_column_headers(
        self,
        table: Locator,
    ) -> list[str]:
        column_header_list: list[Locator] = await table.get_by_role(
            'columnheader').filter(has_not_text='Action').all()
        column_header_str_list: list[str] = []
        for column_header in column_header_list:
            text: str = await column_header.inner_text()
            column_header_str_list.append(text)
        return column_header_str_list

    async def _parse_table_row(
        self,
        page: Page,
        tbody: Locator,
        column_headers: list[str] = [''],
    ) -> TableData:
        tr_list: list[Locator] = await tbody.locator('tr').all()
        table_data_list: TableData = list()
        for tr in tr_list:
            td_list: list[Locator] = await tr.locator('td').filter(
                has_not=page.locator('a')).all()
            td_text_list: list[str] = [
                await td.inner_text() for td in td_list]
            row_data_dict: dict[str, str] = dict(
                zip(column_headers, td_text_list))
            table_data_list.append(row_data_dict)
        return table_data_list

    async def _click_buttons(self, page: Page) -> bool:
        div: Locator = page.locator('div.large-2.columns')
        buttons: list[Locator] = await div.get_by_role('link').all()
        if buttons:
            self.logger.info(
                f'Found {len(buttons)} buttons.'
                 ' Clicking buttons with a 1.5 secs delay interval...'
            )
        for button in buttons:
            await asyncio.sleep(1.5)
            await button.click()
            canvas_num = await self._extract_script_info(page=page)
            self.logger.info(
                f'Clicked button, newly generated answer is {canvas_num}...'
            )
        return True
            
    async def _extract_script_info(self, page: Page) -> str:
        div = page.locator('div#content')
        script = div.locator('script')
        # Another way of doing this:
        # script_code: str = await script.evaluate('''
        #     script => script.text 
        # ''')
        script_code: str = await script.inner_html()
        found: Match[str]|None = re.search(r'Answer: ([0-9]+)', script_code)
        if not found:
            raise ValueError('Could not extract string via regex.')
        canvas_num: str = found.group(1)
        return canvas_num
    
    
    
