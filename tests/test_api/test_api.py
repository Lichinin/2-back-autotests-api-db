import allure

from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from schemas.schemas import PostModel, DeletePostModel


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('API tests')
class TestApi:

    @allure.story('Получить все посты')
    @allure.title('Проверка получения всех постов')
    def test_get_all_posts(self, api_client):
        response = api_client.get_all_posts()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )

    @allure.story('Получить пост')
    @allure.title('Проверка получения поста по его ID')
    def test_get_post_by_id(self, setup_post, api_client):
        response = api_client.get_post_by_id(setup_post['id'])
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )

    @allure.story('Создать пост')
    @allure.title('Проверка создания поста')
    def test_create_post(self, api_client, db_connection, delete_created_post):
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
    @allure.title('Проверка редактирования поста')
    def test_patch_post(self, api_client, setup_post, db_connection):
        response = api_client.patch_post(setup_post['id'], DataHelper.updated_post_data(setup_post))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        AssertionHelper.check_element_from_db(response.json(), db_connection)

    @allure.story('Удалить пост')
    @allure.title('Проверка удаления поста')
    def test_delete_post(self, api_client, created_post):
        response = api_client.delete_post(created_post['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeletePostModel,
                response.json(),
            )
