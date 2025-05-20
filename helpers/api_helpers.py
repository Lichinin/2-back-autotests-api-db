import logging

import allure


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
        except Exception as e:
            error_msg = f'Validation error: {str(e)}'
            logger.error(error_msg)
            raise AssertionError(error_msg)


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
    @allure.step('Получить и проверить элемент в базе данных')
    def check_element_from_db(
        created_element,
        db
    ):
        logger = logging.getLogger('Get element form database')
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
