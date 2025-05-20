import allure
import pytest

from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from schemas.schemas import DeletePostModel, PostModel, CommentModel, DeleteCommentModel
from api_client.api_client import ApiClient


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с постами')
class TestPostsApi:

    @allure.story('Получить все посты')
    @allure.title('POSTS_API_01: Проверка получения всех постов')
    @pytest.mark.parametrize("setup_post", [3], indirect=True)
    def test_get_all_posts(self, setup_post, api_client: ApiClient):
        response = api_client.get_all_posts()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )

    @allure.story('Получить пост')
    @allure.title('POSTS_API_02: Проверка получения поста по его ID')
    def test_get_post_by_id(self, setup_post, api_client: ApiClient):
        response = api_client.get_post_by_id(setup_post['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )

    @allure.story('Создать пост')
    @allure.title('POSTS_API_03: Проверка создания поста')
    def test_create_post(self, api_client: ApiClient, db_connection, delete_created_post):
        response = api_client.create_post(DataHelper.post_setup_data())
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        AssertionHelper.check_element_from_db(response.json(), db_connection)
        delete_created_post(response.json()['id'])

    @allure.story('Редактировать пост')
    @allure.title('POSTS_API_04: Проверка редактирования поста')
    def test_patch_post(self, api_client: ApiClient, setup_post, db_connection):
        response = api_client.patch_post(setup_post['id'], DataHelper.updated_post_data(setup_post))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        AssertionHelper.check_element_from_db(response.json(), db_connection)

    @allure.story('Удалить пост')
    @allure.title('POSTS_API_05: Проверка удаления поста')
    def test_delete_post(self, api_client: ApiClient, created_post):
        response = api_client.delete_post(created_post['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeletePostModel,
                response.json(),
            )
        with allure.step('Проверить данные удалённого поста'):
            assert response.json()['deleted'] is True
            assert response.json()['previous']['id'] == created_post['id']


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с комментариями')
class TestCommentsApi:

    @allure.story('Получить все комментарии')
    @allure.title('COMMENTS_API_01: Проверка получения всех комментариев')
    def test_get_all_comments(self, api_client: ApiClient):
        response = api_client.get_all_comments()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )

    @allure.story('Получить комментарий')
    @allure.title('COMMENTS_API_02: Проверка получения комментария по его ID')
    def test_get_comment_by_id(self, api_client: ApiClient):
        response = api_client.get_comment_by_id(2)
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )

    @allure.story('Создать комментарий')
    @allure.title('COMMENTS_API_03: Проверка создания комментария')
    def test_create_comment(self, setup_post, api_client: ApiClient):
        response = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id']))
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )

    @allure.story('Удалить комментарий')
    @allure.title('COMMENTS_API_05: Проверка удаления комментария')
    def test_delete_comment(self, setup_post, api_client: ApiClient):
        comment = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.delete_comment(comment['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeleteCommentModel,
                response.json(),
            )
