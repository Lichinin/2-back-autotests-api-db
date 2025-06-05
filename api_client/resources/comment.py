import allure
import requests

from api_client.base_api_client import BaseApiClient
from config import APiRoutes


class CommentClient(BaseApiClient):

    @allure.step('Получить список всех комментариев')
    def get_all_comments(self) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/comments'
        return self._get(url)

    @allure.step('Получить комментарий по id')
    def get_comment_by_id(self, comment_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/comments/{comment_id}'
        return self._get(url)

    @allure.step('Создать комментарий')
    def create_comment(self, comment_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/comments'
        return self._post(url, json=comment_data)

    @allure.step('Удалить комментарий по ID')
    def delete_comment(self, post_id: int) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/comments/{post_id}?force=true'
        return self._delete(url)

    @allure.step('Редактировать комментарий по ID')
    def patch_comment(self, id: int, comment_data: dict) -> requests.Response:
        url = f'{APiRoutes.BASE_URL}{APiRoutes.API_VER}/comments/{id}'
        return self._patch(url, json=comment_data)
