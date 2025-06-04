import logging

import allure

from helpers.db_helper import DatabaseHelper


class CommentDbClient:

    def __init__(self, db: DatabaseHelper):
        self.db = db

    @allure.step('Получить комментарий в базе данных')
    def get_comment_by_id(
        self,
        created_element: dict,
    ):
        logger = logging.getLogger('Get comment form database')
        logger.info('* Execute query')
        query = self.db.execute_query(
            f"SELECT * FROM wp_comments WHERE comment_ID = {created_element['id']}",
        )
        return query

    def create_comment_in_db(self, post_data: dict):
        pass

    def delete_comment_by_id(self, post_id: int):
        pass
