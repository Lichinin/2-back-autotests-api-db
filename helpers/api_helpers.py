import logging

import allure
from pydantic import ValidationError


class ValidationHelper:

    @staticmethod
    @allure.step('Проверить схему JSON-ответа')
    def validate_via_pydantic(
        model: type,
        response_data: dict | list
    ) -> None:
        logger = logging.getLogger(f'validation.{model.__name__}')
        logger.info('* Check response scheme')
        try:
            if isinstance(response_data, dict):
                model(**response_data)
            elif isinstance(response_data, list):
                for unit in response_data:
                    model(**unit)
            logger.info(f'entity data: {response_data}')
            logger.info('* Scheme is valid.')
        except ValidationError as e:
            error_msg = f'Validation error: {str(e)}'
            logger.error(error_msg)
            raise AssertionError(error_msg) from e


class AssertionHelper:

    @staticmethod
    @allure.step('Проверить статус-код ответа')
    def check_status_code(
        actual_status_code: int,
        expected_status_code: int
    ):
        assert actual_status_code == expected_status_code, \
                f'Excepted status code {expected_status_code}, got {actual_status_code}'

    @staticmethod
    @allure.step('Проверить пост в базе данных')
    def assert_post_from_db(
        api_element: dict,
        db_element: dict
    ):
        logger = logging.getLogger('Assert post form database')
        logger.info(f'* Assert {api_element["id"]} == {db_element["ID"]}')
        assert api_element['id'] == db_element['ID']
        logger.info(f'* Assert {api_element["title"]["raw"]} == {db_element["post_title"]}')
        assert api_element['title']['raw'] == db_element['post_title']
        logger.info(f'* Assert {api_element["content"]["raw"]} == {db_element["post_content"]}')
        assert api_element["content"]["raw"] == db_element['post_content']

    @staticmethod
    @allure.step('Проверить комментарий в базе данных')
    def assert_comment_from_db(
        api_element: dict,
        db_element: dict
    ):
        logger = logging.getLogger('Assert comment form database')
        logger.info(f'* Assert {api_element["id"]} == {db_element["comment_ID"]}')
        assert api_element['id'] == db_element['comment_ID']
        logger.info(f'* Assert {api_element["author_name"]} == {db_element["comment_author"]}')
        assert api_element['author_name'] == db_element['comment_author']
        logger.info(f'* Assert {api_element["content"]["raw"]} == {db_element["comment_content"]}')
        assert api_element["content"]["raw"] == db_element['comment_content']

    @staticmethod
    @allure.step('Проверить, что созданные для теста комментарии есть в списке полученных')
    def assert_comments_ids(
        created_comments_id: list,
        all_commmets: list
    ):
        logger = logging.getLogger('assert created comments ids in all comments id')
        all_comments_ids = [comment['id'] for comment in all_commmets.json()]
        for id in created_comments_id:
            logger.info(f'* Assert comment_id={id} in id_list={all_comments_ids}')
            assert id in all_comments_ids

    @staticmethod
    @allure.step('Получить и проверить пользователя в базе данных')
    def assert_user_from_db(
        api_element: dict,
        db_element: dict
    ):
        logger = logging.getLogger('Assert user form database')
        logger.info(f'* Assert {api_element["id"]} == {db_element["ID"]}')
        assert api_element['id'] == db_element['ID']
        logger.info(f'* Assert {api_element["name"]} == {db_element["display_name"]}')
        assert api_element['name'] == db_element['display_name']
        logger.info(f'* Assert {api_element["slug"]} == {db_element["user_nicename"]}')
        assert api_element["slug"] == db_element['user_nicename']
        logger.info(f'* Assert {api_element["email"]} == {db_element["user_email"]}')
        assert api_element['email'] == db_element['user_email']
