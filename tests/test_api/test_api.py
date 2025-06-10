import allure
import pytest

from api_client.api_client import ApiClient
from helpers.api_helpers import AssertionHelper, ValidationHelper
from helpers.data_helpers import DataHelper
from helpers.db_clients.comment_db_client import CommentDbClient
from helpers.db_clients.post_db_client import PostDbClient
from helpers.db_clients.user_db_client import UserDbClient
from helpers.db_helper import DatabaseHelper
from schemas.schemas import (CommentModel, DeleteCommentModel, DeletePostModel,
                             DeleteUserModel, PostModel, UserGetModel,
                             UserPostModel)


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с постами')
class TestPostsApi:

    @allure.story('Получить все посты')
    @allure.title('POSTS_API_01: Проверка получения всех постов')
    @pytest.mark.parametrize("setup_post", [3], indirect=True)
    def test_get_all_posts(self, setup_post: list, api_client: ApiClient):
        response = api_client.posts.get_all_posts()
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
        response = api_client.posts.get_post_by_id(setup_post['id'])
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
        response = api_client.posts.create_post(DataHelper.post_setup_data())
        posts_to_delete_list.append(response.json())
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Получить пост из БД'):
            post_db_client = PostDbClient(db_connection)
            db_post = post_db_client.get_post_by_id(
                response.json()
            )
        with allure.step('Проверить данные поста в БД'):
            AssertionHelper.assert_post_from_db(
                response.json(),
                db_post
            )

    @allure.story('Редактировать пост')
    @allure.title('POSTS_API_04: Проверка редактирования поста')
    def test_patch_post(
        self,
        api_client: ApiClient,
        setup_post: dict,
        db_connection: DatabaseHelper
    ):
        response = api_client.posts.patch_post(setup_post['id'], DataHelper.updated_post_data(setup_post))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Получить пост из БД'):
            post_db_client = PostDbClient(db_connection)
            db_post = post_db_client.get_post_by_id(
                response.json()
            )
        with allure.step('Проверить данные поста в БД'):
            AssertionHelper.assert_post_from_db(
                response.json(),
                db_post
            )

    @allure.story('Удалить пост')
    @allure.title('POSTS_API_05: Проверка удаления поста')
    def test_delete_post(self, api_client: ApiClient, created_post: dict):
        response = api_client.posts.delete_post(created_post['id'])
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
            created_comments_ids = DataHelper.create_comments_id_list(setup_post, api_client)
        response = api_client.comments.get_all_comments()
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
            comment = api_client.comments.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.comments.get_comment_by_id(comment['id'])
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
        response = api_client.comments.create_comment(DataHelper.comment_setup_data(setup_post['id']))
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Получить комментарий из БД'):
            comment_db_client = CommentDbClient(db_connection)
            db_comment = comment_db_client.get_comment_by_id(
                response.json()
            )
        with allure.step('Проверить данные комментария в БД'):
            AssertionHelper.assert_comment_from_db(
                response.json(),
                db_comment
            )

    @allure.story('Редактировать комментарий')
    @allure.title('COMMENTS_API_04: Проверка редактирования комментария')
    def test_patch_comment(
        self,
        api_client: ApiClient,
        setup_post: dict,
        db_connection: DatabaseHelper,
    ):
        with allure.step('Создать комментарий для теста'):
            comment = api_client.comments.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.comments.patch_comment(comment['id'], DataHelper.updated_comment_data(comment))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Получить комментарий из БД'):
            comment_db_client = CommentDbClient(db_connection)
            db_comment = comment_db_client.get_comment_by_id(
                response.json()
            )
        with allure.step('Проверить данные комментария в БД'):
            AssertionHelper.assert_comment_from_db(
                response.json(),
                db_comment
            )

    @allure.story('Удалить комментарий')
    @allure.title('COMMENTS_API_05: Проверка удаления комментария')
    def test_delete_comment(self, setup_post: dict, api_client: ApiClient):
        with allure.step('Создать комментарий для теста'):
            comment = api_client.comments.create_comment(DataHelper.comment_setup_data(setup_post['id'])).json()
        response = api_client.comments.delete_comment(comment['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeleteCommentModel,
                response.json(),
            )
        with allure.step('Проверить данные удалённого комментария'):
            assert response.json()['deleted'] is True
            assert response.json()['previous']['id'] == comment['id']


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с пользователями')
class TestUsersApi:

    @allure.story('Получить список всех пользователей')
    @allure.title('USERS_API_01: Проверка получения списка всех пользователей')
    @pytest.mark.parametrize("setup_user", [3], indirect=True)
    def test_get_all_users(self, setup_user, api_client: ApiClient):
        response = api_client.users.get_all_users()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserGetModel,
                response.json(),
            )
        with allure.step('Проверить, что список пользователей содержит нужное количество записей'):
            assert len(response.json()) >= len(setup_user), \
                f'Ожидается минимум {len(setup_user)} пользователей, получено {len(response.json())}'

    @allure.story('Получить пользователя')
    @allure.title('USERS_API_02: Проверка получения пользователя по его ID')
    def test_get_user_by_id(self, setup_user: dict, api_client: ApiClient):
        response = api_client.users.get_user_by_id(setup_user['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserGetModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемого пользователя'):
            assert response.json()['id'] == setup_user['id'], \
                f'Ожидается пользователь с id = {setup_user["id"]}, получен пользователь с id = {response.json()["id"]}'

    @allure.story('Создать пользователя')
    @allure.title('USERS_API_03: Проверка создания пользователя')
    def test_create_user(
        self,
        api_client: ApiClient,
        db_connection: DatabaseHelper,
        users_to_delete_list: list
    ):
        response = api_client.users.create_user(DataHelper.user_setup_data())
        users_to_delete_list.append(response.json())
        AssertionHelper.check_status_code(response.status_code, 201)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserPostModel,
                response.json(),
            )
        with allure.step('Получить пользователя из БД'):
            user_db_client = UserDbClient(db_connection)
            db_user = user_db_client.get_user_by_id(
                response.json()
            )
        with allure.step('Проверить данные пользователя в БД'):
            AssertionHelper.assert_user_from_db(
                response.json(),
                db_user
            )

    @allure.story('Редактировать пользователя')
    @allure.title('USERS_API_04: Проверка редактирования пользователя')
    def test_patch_user(
        self,
        api_client: ApiClient,
        setup_user: dict,
        db_connection: DatabaseHelper
    ):
        response = api_client.users.patch_user(setup_user['id'], DataHelper.updated_user_data(setup_user))
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserPostModel,
                response.json(),
            )
        with allure.step('Получить пользователя из БД'):
            user_db_client = UserDbClient(db_connection)
            db_user = user_db_client.get_user_by_id(
                response.json()
            )
        with allure.step('Проверить данные пользователя в БД'):
            AssertionHelper.assert_user_from_db(
                response.json(),
                db_user
            )

    @allure.story('Удалить пользователя')
    @allure.title('USERS_API_05: Проверка удаления пользователя')
    def test_delete_user(self, created_user: dict, api_client: ApiClient):
        response = api_client.users.delete_user(created_user['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                DeleteUserModel,
                response.json(),
            )
        with allure.step('Проверить данные удалённого пользователя'):
            assert response.json()['deleted'] is True
            assert response.json()['previous']['id'] == created_user['id']


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с постами. Работа с данными через DB')
class TestPostDb:

    @allure.story('Получить все посты, созданные через SQL')
    @allure.title('POSTS_DB_01: Проверка получения всех постов, созданных через SQL')
    @pytest.mark.parametrize("setup_post_by_db", [3], indirect=True)
    def test_get_all_posts_db(self, setup_post_by_db: list, api_client: ApiClient):
        response = api_client.posts.get_all_posts()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить, что список постов содержит нужное количество записей'):
            assert len(response.json()) >= len(setup_post_by_db), \
                f'Ожидается минимум {len(setup_post_by_db)} постов, получено {len(response.json())}'

    @allure.story('Получить пост, созданный через SQL')
    @allure.title('POSTS_DB_02: Проверка получения поста по его ID, созданного через SQL')
    def test_get_post_by_id_db(self, setup_post_by_db: dict, api_client: ApiClient):
        response = api_client.posts.get_post_by_id(setup_post_by_db['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                PostModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемый пост'):
            assert response.json()['id'] == setup_post_by_db['id'], \
                f'Ожидается пост с id = {setup_post_by_db["id"]}, получен пост с id = {response.json()["id"]}'
            assert response.json()['title']['rendered'] == setup_post_by_db['title'], \
                f'Ожидается title = {setup_post_by_db["title"]}, получен title = {response.json()["title"]["rendered"]}'


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с пользователями. Работа с данными через DB')
class TestUserDb:

    @allure.story('Получить всех пользователей, созданных через SQL')
    @allure.title('POSTS_DB_01: Проверка получения всех пользователей, созданных через SQL')
    @pytest.mark.parametrize("setup_user_by_db", [3], indirect=True)
    def test_get_all_posts_db(self, setup_user_by_db: list, api_client: ApiClient):
        response = api_client.users.get_all_users()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserGetModel,
                response.json(),
            )
        with allure.step('Проверить, что список пользователей содержит нужное количество записей'):
            assert len(response.json()) >= len(setup_user_by_db), \
                f'Ожидается минимум {len(setup_user_by_db)} постов, получено {len(response.json())}'

    @allure.story('Получить пользователя, созданного через SQL')
    @allure.title('POSTS_DB_02: Проверка получения пользователя по его ID, созданного через SQL')
    def test_get_user_by_id(self, setup_user_by_db: dict, api_client: ApiClient):
        response = api_client.users.get_user_by_id(setup_user_by_db['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                UserGetModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемого пользователя'):
            assert response.json()['id'] == setup_user_by_db['id'], \
                f'Ожидается пользователь с id = {setup_user_by_db["id"]}, получен с id = {response.json()["id"]}'
            assert response.json()['name'] == setup_user_by_db['user_login'], \
                f'Ожидается name = {setup_user_by_db["user_login"]}, получен name = {response.json()["name"]}'


@allure.epic('SimbirSoft SDET практикум. Блок 2. API, DB')
@allure.suite('Тестирование API для работы с комментариями. Работа с данными через DB')
class TestCommentsDb:

    @allure.story('Получить все комментарии, созданные через SQL')
    @allure.title('COMMENTS_DB_01: Проверка получения всех комментариев, созданных через SQL')
    @pytest.mark.parametrize("setup_post", [3], indirect=True)
    def test_get_all_comments(self, setup_post: list, api_client: ApiClient, db_connection):
        with allure.step('Создать комментарии для теста'):
            created_comments_ids = CommentDbClient.create_comments_id_list_db(setup_post, db_connection)
        response = api_client.comments.get_all_comments()
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить что созданные ранее комментарии есть в списке полученных'):
            AssertionHelper.assert_comments_ids(created_comments_ids, response)

    @allure.story('Получить комментарий, созданный через SQL')
    @allure.title('COMMENTS_API_02: Проверка получения комментария, созданного через SQL, по его ID')
    def test_get_comment_by_id(self, setup_post_by_db: dict, api_client: ApiClient, db_connection):
        with allure.step('Создать комментарий для теста'):
            db_clinet = CommentDbClient(db_connection)
            comment = db_clinet.create_comment_in_db(setup_post_by_db)
        response = api_client.comments.get_comment_by_id(comment['id'])
        AssertionHelper.check_status_code(response.status_code, 200)
        with allure.step('Проверить схему ответа с помощью pydantic'):
            ValidationHelper.validate_via_pydantic(
                CommentModel,
                response.json(),
            )
        with allure.step('Проверить, что получили ожидаемый комментарий'):
            assert response.json()['id'] == comment['id'], \
                f'Ожидается комментарий с id={comment["id"]}, получен комментарий с id={response.json()["id"]}'
            assert response.json()['author_name'] == comment['comment_author'], \
                f'Ожидается author_name={comment["comment_author"]}, получен {response.json()["author_name"]}'
