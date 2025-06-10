import logging

import allure

from helpers.data_helpers import DbDataHelper
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
        logger = logging.getLogger('Creaty comment by SQL')
        logger.info('* Execute query')

        data = DbDataHelper.prepare_comment_data(post_data['id'])

        query = """
            INSERT INTO wp_comments (
                comment_date,
                comment_date_gmt,
                comment_post_ID,
                comment_author,
                comment_author_email,
                comment_content
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = tuple(data.values())

        comment_id = self.db.insert_and_get_lastrowid(query, params)
        logger.info(f'Comment with ID={comment_id} was created')

        return {
            'id': comment_id,
            'comment_author': data['comment_author'],
            'comment_author_email': data['comment_author_email'],
            'comment_content': data['comment_content']
        }

    def delete_comments_by_post_id(self, post_id: int):
        logger = logging.getLogger('Delete comments by post ID')
        logger.info('* Execute query')

        query = "DELETE FROM wp_comments WHERE comment_post_ID = %s"
        params = (post_id,)

        self.db.execute_query(query, params)
        self.db.connection.commit()
        logger.info(f'Комментарии для поста {post_id} успешно удалены')

    @staticmethod
    @allure.step('Подготовить комментарии для теста и вернуть список их ID')
    def create_comments_id_list_db(posts: list, db_connection) -> list:
        created_comments_ids = []
        db_client = CommentDbClient(db_connection)
        for post in posts:
            comment = db_client.create_comment_in_db(post)
            created_comments_ids.append(comment['id'])
        return created_comments_ids
