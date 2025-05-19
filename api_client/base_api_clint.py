import base64
import logging

import allure
import requests
from requests.exceptions import RequestException

from authconfig import AuthConfig


class BaseApiClient:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.auth_token = self._generate_basic_auth_token()

    def _generate_basic_auth_token(self) -> str:
        credentials = f"{AuthConfig.USERNAME}:{AuthConfig.PASSWORD}"
        return base64.b64encode(credentials.encode()).decode('utf-8')

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

    @allure.step('Выполнить POST запрос')
    def _post(
        self,
        url: str,
        json: dict,
        headers: dict = None
    ) -> requests.Response:
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.auth_token}"
            }
        else:
            headers["Authorization"] = f"Basic {self.auth_token}"
        return self._make_request('POST', url, headers=headers, json=json)

    @allure.step('Выполнить PATCH запрос')
    def _patch(
        self,
        url: str,
        json: dict,
        headers: dict = None
    ) -> requests.Response:
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.auth_token}"
            }
        else:
            headers["Authorization"] = f"Basic {self.auth_token}"
        return self._make_request('PATCH', url, headers=headers, json=json)

    @allure.step('Выполнить DELETE запрос')
    def _delete(
        self,
        url: str,
        headers: dict = None
    ) -> requests.Response:
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.auth_token}"
            }
        else:
            headers["Authorization"] = f"Basic {self.auth_token}"
        return self._make_request('DELETE', url, headers=headers)
