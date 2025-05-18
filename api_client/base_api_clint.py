import logging

import allure
import requests
from requests.exceptions import RequestException


class BaseApiClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step('Выполнить {method} запрос на {url}')
    def _make_request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        json: dict = None
    ) -> requests.Response:
        try:
            self.logger.info(f'Send {method} request to {url}')
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json
            )
            response.raise_for_status()
            return response
        except RequestException:
            self.logger.error(f'Failed {method} request to {url} ')
            raise Exception(
                f'Failed {method} request to {url} '
            )

    @allure.step('Выполнить GET запрос')
    def _get(self, url: str) -> requests.Response:
        return self._make_request('GET', url)
