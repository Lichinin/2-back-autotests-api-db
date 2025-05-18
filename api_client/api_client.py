import allure
import requests

from api_client.base_api_clint import BaseApiClient
from config import APiRoutes


class ApiClient(BaseApiClient):

    @allure.step('Получить список всех сущностей')
    def get_all_posts(self) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts'
        return self._get(url)

    @allure.step('Получить список всех сущностей')
    def get_post_by_id(self, post_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts/{post_id}'
        return self._get(url)
