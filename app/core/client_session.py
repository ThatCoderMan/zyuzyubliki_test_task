import logging
from http import HTTPStatus

import aiohttp
from aiohttp.client_exceptions import ClientError
from fake_useragent import UserAgent


class ClientSession:
    def __init__(self, headers=None):
        ua = UserAgent()
        self.headers = {"User-Agent": ua.random}
        if headers:
            self.headers.update(headers)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_data(self, link):
        """Асинхронное получение данных по ссылке."""
        status_code = -1
        try:
            async with self.session.get(link, timeout=10) as response:
                status_code = response.status
                if response.status == HTTPStatus.OK:
                    logging.info(f'Response [{status_code}]: {link}')
                    return await response.content.read()
                response.raise_for_status()
        except TimeoutError:
            logging.warning(f'Response [{status_code}] - TimeoutError: {link}')
        except ClientError as exception:
            logging.warning(
                f'Response [{status_code}] - ClientError: {link} - {exception}'
            )
        except Exception as exception:
            logging.error(f'Response [{status_code}]: {link} - {exception}')
        return False
