import logging

import allure

from helpers.data_helpers import DbDataHelper
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

    def create_user_in_db(self):
        logger = logging.getLogger('Creaty post by SQL')
        logger.info('* Execute query')

        data = DbDataHelper.prepare_user_data()

        query = """
            INSERT INTO wp_users (
                user_registered,
                user_login,
                user_email,
                user_pass,
                display_name
            ) VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            data['user_registered'],
            data['user_login'],
            data['user_email'],
            data['user_pass'],
            data['display_name']
            )

        user_id = self.db.insert_and_get_lastrowid(query, params)
        logger.info(f'User with ID={user_id} was created')

        return {
            'id': user_id,
            'user_login': data['user_login'],
            'user_email': data['user_email'],
            'display_name': data['display_name']
        }

    def delete_user_by_id_db(self, user_id: int):
        logger = logging.getLogger('Delete post by ID (SQL)')
        logger.info('* Execute query')

        query = "DELETE FROM wp_users WHERE ID = %s"
        params = (user_id,)

        self.db.execute_query(query, params)
        self.db.connection.commit()
        logger.info(f'Пост с ID={user_id} успешно удален из БД')
