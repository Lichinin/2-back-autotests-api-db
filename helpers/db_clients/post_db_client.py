import logging

import allure

from helpers.data_helpers import DbDataHelper
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

    def create_post_in_db(self):
        logger = logging.getLogger('Creaty post by SQL')
        logger.info('* Execute query')

        data = DbDataHelper.prepare_post_data()

        query = """
            INSERT INTO wp_posts (
                post_date,
                post_date_gmt,
                post_modified,
                post_modified_gmt,
                post_content,
                post_title,
                post_name,
                post_excerpt,
                post_status,
                to_ping,
                pinged,
                post_content_filtered
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['post_date'],
            data['post_date_gmt'],
            data['post_modified'],
            data['post_modified_gmt'],
            data['post_content'],
            data['post_title'],
            data['post_name'],
            data['post_excerpt'],
            data['post_status'],
            data['to_ping'],
            data['pinged'],
            data['post_content_filtered']
            )

        post_id = self.db.insert_and_get_lastrowid(query, params)
        logger.info(f'Post with ID={post_id} was created')

        return {
            'id': post_id,
            'title': data['post_title'],
            'content': data['post_content'],
            'status': data['post_status']
        }

    def delete_post_by_id_db(self, post_id: int):
        logger = logging.getLogger('Delete post by ID (SQL)')
        logger.info('* Execute query')

        query = "DELETE FROM wp_posts WHERE ID = %s"
        params = (post_id,)

        self.db.execute_query(query, params)
        self.db.connection.commit()
        logger.info(f'Пост с ID={post_id} успешно удален из БД')
