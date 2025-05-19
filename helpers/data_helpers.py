import allure
from faker import Faker

fake = Faker()


class DataHelper:

    @staticmethod
    @allure.step('Сформировать значения полей нового поста')
    def post_setup_data() -> dict:
        return {
            "title": fake.sentence(),
            "content": fake.sentence(),
            "status": "publish"
        }

    @staticmethod
    @allure.step('Сформировать новые значения полей для существующего поста')
    def updated_post_data(post_data) -> dict:
        return {
            "title": f'Updated_{post_data["title"]["raw"]}',
            "content": f'Updated_{post_data["content"]["raw"]}'
        }
