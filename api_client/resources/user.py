import allure
import requests

from api_client.base_api_clint import BaseApiClient
from config import APiRoutes


class UserClient(BaseApiClient):

    @allure.step('Получить список всех пользователей')
    def get_all_users(self) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/users'
        return self._get(url)

    @allure.step('Получить пользователя по id')
    def get_user_by_id(self, post_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/users/{post_id}'
        return self._get(url)

    @allure.step('Создать пост')
    def create_user(self, user_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/users'

        return self._post(url, json=user_data)

    @allure.step('Редактировать пользователя по ID')
    def patch_user(self, id: int, user_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/users/{id}'
        return self._patch(url, json=user_data)

    @allure.step('Удалить пользователя по ID')
    def delete_user(self, user_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/users/{user_id}?reassign=1&force=true'
        return self._delete(url)
