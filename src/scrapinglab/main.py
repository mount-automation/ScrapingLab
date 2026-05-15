import asyncio
from playwright.async_api import async_playwright
from scrapinglab.extension_1 import Extension1

async def main_init():
    async with (
        async_playwright() as p,
        await p.chromium.launch(headless=False) as browser,
    ):
        ext_list = [Extension1(browser=browser)]
        try:
            async with asyncio.TaskGroup() as tg:
                for ext in ext_list:
                    tg.create_task(ext.init_extension())
        except ExceptionGroup as eg:
            for e in eg.exceptions:
                print(f'Next...\n{e}')

def main():
    asyncio.run(main_init())

if __name__ == '__main__':
    main()