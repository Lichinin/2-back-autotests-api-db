import logging

import allure

from helpers.db_helper import DatabaseHelper


class PostDbClient:

    def __init__(self, db: DatabaseHelper):
        self.db = db

    @allure.step('Получить пост в базе данных')
    def get_post_by_id(
        self,
        created_element: dict,
    ):
        logger = logging.getLogger('Get post form database')
        logger.info('* Execute query')
        query = self.db.execute_query(
            f"SELECT * FROM wp_posts WHERE id = {created_element['id']}",
        )
        return query

    def create_post_in_db(self, post_data: dict):
        pass

    def delete_post_by_id(self, post_id: int):
        pass
