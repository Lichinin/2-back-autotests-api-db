import logging

import allure
from pydantic import ValidationError

from helpers.db_helper import DatabaseHelper


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
    @allure.step('Получить и проверить пост в базе данных')
    def assert_post_from_db(
        created_element: dict,
        db: DatabaseHelper
    ):
        logger = logging.getLogger('Get post form database')
        logger.info('* Execute query')
        result = db.execute_query(
            f"SELECT * FROM wp_posts WHERE id = {created_element['id']}",
        )
        logger.info(f'* Assert {created_element["id"]} == {result["ID"]}')
        assert created_element['id'] == result['ID']
        logger.info(f'* Assert {created_element["title"]["raw"]} == {result["post_title"]}')
        assert created_element['title']['raw'] == result['post_title']
        logger.info(f'* Assert {created_element["content"]["raw"]} == {result["post_content"]}')
        assert created_element["content"]["raw"] == result['post_content']

    @staticmethod
    @allure.step('Получить и проверить комментарий в базе данных')
    def assert_comment_from_db(
        created_element: dict,
        db: DatabaseHelper
    ):
        logger = logging.getLogger('Get comment form database')
        logger.info('* Execute query')
        result = db.execute_query(
            f"SELECT * FROM wp_comments WHERE comment_id = {created_element['id']}",
        )
        logger.info(f'* Assert {created_element["id"]} == {result["comment_ID"]}')
        assert created_element['id'] == result['comment_ID']
        logger.info(f'* Assert {created_element["author_name"]} == {result["comment_author"]}')
        assert created_element['author_name'] == result['comment_author']
        logger.info(f'* Assert {created_element["content"]["raw"]} == {result["comment_content"]}')
        assert created_element["content"]["raw"] == result['comment_content']

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
