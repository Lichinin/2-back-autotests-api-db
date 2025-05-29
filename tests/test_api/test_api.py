import allure
import pytest

from api_client.api_client import ApiClient
from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from helpers.db_helper import DatabaseHelper
from schemas.schemas import (CommentModel, DeleteCommentModel, DeletePostModel,
                             PostModel)


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с постами')
class TestPostsApi:

    @allure.story('Получить все посты')
    @allure.title('POSTS_API_01: Проверка получения всех постов')
    @pytest.mark.parametrize("setup_post", [3], indirect=True)
    def test_get_all_posts(self, setup_post: list, api_client: ApiClient):
        response = api_client.get_all_posts()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить, что список постов содержит нужное количество записей'):
            assert len(response.json()) >= len(setup_post), \
                f'Ожидается минимум {len(setup_post)} постов, получено {len(response.json())}'

    @allure.story('Получить пост')
    @allure.title('POSTS_API_02: Проверка получения поста по его ID')
    def test_get_post_by_id(self, setup_post: dict, api_client: ApiClient):
        response = api_client.get_post_by_id(setup_post['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемый пост'):
            assert response.json()['id'] == setup_post['id'], \
                f'Ожидается пост с id = {setup_post["id"]}, получен пост с id = {response.json()["id"]}'

    @allure.story('Создать пост')
    @allure.title('POSTS_API_03: Проверка создания поста')
    def test_create_post(
        self,
        api_client: ApiClient,
        db_connection: DatabaseHelper,
        posts_to_delete_list: list
    ):
        response = api_client.create_post(DataHelper.post_setup_data())
        posts_to_delete_list.append(response.json())
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить данные поста в БД'):
            AssertionHelper.assert_post_from_db(response.json(), db_connection)

    @allure.story('Редактировать пост')
    @allure.title('POSTS_API_04: Проверка редактирования поста')
    def test_patch_post(
        self,
        api_client: ApiClient,
        setup_post: dict,
        db_connection: DatabaseHelper
    ):
        response = api_client.patch_post(setup_post['id'], DataHelper.updated_post_data(setup_post))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить данные поста в БД'):
            AssertionHelper.assert_post_from_db(response.json(), db_connection)

    @allure.story('Удалить пост')
    @allure.title('POSTS_API_05: Проверка удаления поста')
    def test_delete_post(self, api_client: ApiClient, created_post: dict):
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
    @pytest.mark.parametrize("setup_post", [3], indirect=True)
    def test_get_all_comments(self, setup_post: list, api_client: ApiClient):
        with allure.step('Создать комментарии для теста'):
            created_comments_ids = []
            for post in setup_post:
                comment = api_client.create_comment(DataHelper.comment_setup_data(post['id'])).json()
                created_comments_ids.append(comment['id'])
        response = api_client.get_all_comments()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить что созданные ранее комментарии есть в списке полученных'):
            AssertionHelper.assert_comments_ids(created_comments_ids, response)

    @allure.story('Получить комментарий')
    @allure.title('COMMENTS_API_02: Проверка получения комментария по его ID')
    def test_get_comment_by_id(self, setup_post: dict, api_client: ApiClient):
        with allure.step('Создать комментарий для теста'):
            comment = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.get_comment_by_id(comment['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемый комментарий'):
            assert response.json()['id'] == comment['id'], \
                f'Ожидается комментарий с id={comment["id"]}, получен комментарий с id={response.json()["id"]}'

    @allure.story('Создать комментарий')
    @allure.title('COMMENTS_API_03: Проверка создания комментария')
    def test_create_comment(
        self,
        setup_post: dict,
        api_client: ApiClient,
        db_connection: DatabaseHelper
    ):
        response = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id']))
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить данные комментария в БД'):
            AssertionHelper.assert_comment_from_db(response.json(), db_connection)

    @allure.story('Редактировать комментарий')
    @allure.title('COMMENTS_API_04: Проверка редактирования комментария')
    def test_patch_comment(
        self,
        api_client: ApiClient,
        setup_post: dict,
        db_connection: DatabaseHelper,
    ):
        with allure.step('Создать комментарий для теста'):
            comment = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.patch_comment(comment['id'], DataHelper.updated_comment_data(comment))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить данные комментария в БД'):
            AssertionHelper.assert_comment_from_db(response.json(), db_connection)

    @allure.story('Удалить комментарий')
    @allure.title('COMMENTS_API_05: Проверка удаления комментария')
    def test_delete_comment(self, setup_post: dict, api_client: ApiClient):
        with allure.step('Создать комментарий для теста'):
            comment = api_client.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.delete_comment(comment['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeleteCommentModel,
                response.json(),
            )
        with allure.step('Проверить данные удалённого комментария'):
            assert response.json()['deleted'] is True
            assert response.json()['previous']['id'] == comment['id']
