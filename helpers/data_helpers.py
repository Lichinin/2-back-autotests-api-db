import allure
from faker import Faker

from api_client.api_client import ApiClient

fake = Faker()


class DataHelper:

    @staticmethod
    @allure.step('Сформировать значения полей нового поста')
    def post_setup_data() -> dict:
        return {
            "title": fake.sentence(),
            "content": fake.sentence(),
            "status": "publish"
        }

    @staticmethod
    @allure.step('Сформировать новые значения полей для существующего поста')
    def updated_post_data(post_data: dict) -> dict:
        return {
            "title": f'Updated_{post_data["title"]["raw"]}',
            "content": f'Updated_{post_data["content"]["raw"]}'
        }

    @staticmethod
    @allure.step('Сформировать значения полей нового комментария')
    def comment_setup_data(post_id: int) -> dict:
        return {
            "post": post_id,
            "author_name": fake.sentence(),
            "author_email": fake.email(),
            "content": fake.sentence(),
            "status": "approve"
        }

    @staticmethod
    @allure.step('Сформировать новые значения полей для существующего комментария')
    def updated_comment_data(comment_data: dict) -> dict:
        return {
            "content": f'Updated_{comment_data["content"]["raw"]}'
        }

    @staticmethod
    @allure.step('Сформировать значения полей нового пользователя')
    def user_setup_data() -> dict:
        return {
            "username": fake.name(),
            "email": fake.email(),
            "password": fake.password(length=8),
            "roles": ["subscriber"]
        }

    @staticmethod
    @allure.step('Сформировать новые значения полей для существующего пользователя')
    def updated_user_data(user_data: dict) -> dict:
        return {
            "email": f'Updated_{user_data["email"]}',
        }

    @staticmethod
    @allure.step('Подготовить комментарии для теста и вернуть список их ID')
    def create_comments_id_list(posts: list, api_client: ApiClient) -> list:
        created_comments_ids = []
        for post in posts:
            comment = api_client.comments.create_comment(DataHelper.comment_setup_data(post['id'])).json()
            created_comments_ids.append(comment['id'])
        return created_comments_ids
