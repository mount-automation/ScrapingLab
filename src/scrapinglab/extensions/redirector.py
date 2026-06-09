from .core import BaseExtension
from playwright.async_api import (
    Page,
    Locator,
    Request,
    Response,
)

CHAIN = list[str]

class Redirector(BaseExtension):
    url = 'https://the-internet.herokuapp.com/redirector'
    redirect_url = 'https://the-internet.herokuapp.com/status_codes'

    async def run(self, page: Page) -> None:
        await page.goto(self.url)
        link: Locator = page.get_by_role('link', name='here')
        async with (
            page.expect_response(self.redirect_url) as response_info
        ):
            await link.click()
        response: Response = await response_info.value
        await self._trace_redirection_chain(response=response)
    
    async def _trace_redirection_chain(self, response: Response) -> None:
        chain: CHAIN = []
        chain.append(f'{response.url} [{response.status}]')
        request: Request = response.request
        while True:
            prev_request: Request|None = request.redirected_from
            if prev_request:
                prev_response: Response|None = await prev_request.response()
                if not prev_response:
                    raise ValueError(
                        'Cannot acquire response object'
                        ' from previous request.'
                    )
                chain.append(f'{prev_response.url} [{prev_response.status}]')
                request: Request = prev_request
            else:
                break
        chain.reverse()
        self.logger.info(f'Redirection chain: {" -> ".join(chain)}')









            