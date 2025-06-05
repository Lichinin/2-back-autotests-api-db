import logging

import allure

from helpers.db_helper import DatabaseHelper


class UserDbClient:

    def __init__(self, db: DatabaseHelper):
        self.db = db

    @allure.step('Получить пользователя в базе данных')
    def get_user_by_id(
        self,
        created_element: dict,
    ):
        logger = logging.getLogger('Get user form database')
        logger.info('* Execute query')
        query = self.db.execute_query(
            f"SELECT * FROM wp_users WHERE id = {created_element['id']}",
        )
        return query

    def create_user_in_db(self, post_data: dict):
        pass

    def delete_user_by_id(self, post_id: int):
        pass
