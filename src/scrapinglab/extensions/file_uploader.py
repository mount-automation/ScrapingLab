from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    FileChooser,
)
import asyncio

class FileUploader(BaseExtension):
    url = 'https://the-internet.herokuapp.com/upload'
    filepath = r"C:\Users\MaeganMaulder\Downloads\TEST\test_upload.txt"

    async def run(self, page: Page) -> None:
        await page.goto(self.url, timeout=60000)
        choose_file_btn: Locator = page.get_by_role(
            'button', name='Choose File')
        async with(
            choose_file_btn.page.expect_file_chooser() as fc_info
        ):
            await choose_file_btn.click()
        file_chooser: FileChooser = await fc_info.value
        await file_chooser.set_files(self.filepath)
        upload_btn: Locator = page.get_by_role('button', name='Upload')
        await upload_btn.click()
        uploaded_text: Locator = page.locator('div#uploaded-files')
        filename = await uploaded_text.inner_text()
        if filename in self.filepath:
            self.logger.info('File uploaded!')
        else:
            self.logger.info('Something went wrong!')