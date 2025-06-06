import allure
import requests

from api_client.base_api_client import BaseApiClient
from config import APiRoutes


class PostClient(BaseApiClient):

    @allure.step('Получить список всех постов')
    def get_all_posts(self) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts'
        return self._get(url)

    @allure.step('Получить пост по id')
    def get_post_by_id(self, post_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts/{post_id}'
        return self._get(url)

    @allure.step('Создать пост')
    def create_post(self, post_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts'

        return self._post(url, json=post_data)

    @allure.step('Редактировать пост по ID')
    def patch_post(self, id: int, post_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts/{id}'
        return self._patch(url, json=post_data)

    @allure.step('Удалить пост по ID')
    def delete_post(self, post_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/posts/{post_id}?force=true'
        return self._delete(url)
