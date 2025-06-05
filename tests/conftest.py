import logging
from logging.handlers import RotatingFileHandler

import pytest

from api_client.api_client import ApiClient
from config import Paths
from helpers.data_helpers import DataHelper
from helpers.db_clients.user_db_client import UserDbClient
from helpers.db_helper import DatabaseHelper
from helpers.db_clients.post_db_client import PostDbClient


@pytest.fixture(autouse=True)
def configure_logging(request):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    log_dir = Paths.LOG_DIR
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        str(log_dir / f'{request.node.name}.log'),
        maxBytes=30000000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    test_logger = logging.getLogger(request.node.name)
    test_logger.info(f'Test started: {request.node.name}')

    yield

    test_logger.info(f'Test finished: {request.node.name}\n')


@pytest.fixture()
def api_client(request):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture ApiClient started')
    client = ApiClient()

    yield client

    logger.info('====> Fixture ApiClient teardown')


@pytest.fixture
def setup_post(request, api_client):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup started')
    posts_list = []
    num_entities = request.param if hasattr(request, 'param') else 1
    for _ in range(num_entities):
        logger.info('====> Fixture: Try create post for test')
        response = api_client.posts.create_post(DataHelper.post_setup_data())
        logger.info(f'====> Fixture: Successful create post (id={response.json()["id"]}) for test.')
        posts_list.append(response.json())

    yield posts_list[0] if num_entities == 1 else posts_list

    for post in posts_list:
        logger.info(f'====> Fixture: Delete post (id={post["id"]}) for test')
        api_client.posts.delete_post(post['id'])
    logger.info('====> Fixture setup exit')


@pytest.fixture()
def db_connection():
    logger = logging.getLogger('fixture.db_connection')
    logger.info('====> Connect to database')
    with DatabaseHelper() as db:
        yield db


@pytest.fixture()
def posts_to_delete_list(api_client):
    logger = logging.getLogger("fixture.delete_created_post")
    logger.info("====> Setup fixture: delete_created_post")
    posts = []

    yield posts

    for post in posts:
        logger.info(f"====> Teardown: Delete post with ID={post['id']}")
        api_client.posts.delete_post(post['id'])


@pytest.fixture
def created_post(api_client):
    logger = logging.getLogger("fixture.created_post")
    logger.info('====> Creating single post')

    response = api_client.posts.create_post(DataHelper.post_setup_data())
    post_data = response.json()
    logger.info(f'====> Created post with ID={post_data["id"]}')

    return post_data


@pytest.fixture()
def users_to_delete_list(api_client):
    logger = logging.getLogger("fixture.users_to_delete_list")
    logger.info("====> Setup fixture: users_to_delete_list")
    users = []

    yield users

    for user in users:
        logger.info(f"====> Teardown: Delete user with ID={user['id']}")
        api_client.users.delete_user(user['id'])


@pytest.fixture
def created_user(api_client):
    logger = logging.getLogger("fixture.created_user")
    logger.info('====> Creating single user')

    response = api_client.users.create_user(DataHelper.user_setup_data())
    user_data = response.json()
    logger.info(f'====> Created post with ID={user_data["id"]}')

    return user_data


@pytest.fixture
def setup_user(request, api_client):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup started')
    users_list = []
    num_entities = request.param if hasattr(request, 'param') else 1
    for _ in range(num_entities):
        logger.info('====> Fixture: Try create user for test')
        response = api_client.users.create_user(DataHelper.user_setup_data())
        logger.info(f'====> Fixture: Successful create user (id={response.json()["id"]}) for test.')
        users_list.append(response.json())

    yield users_list[0] if num_entities == 1 else users_list

    for user in users_list:
        logger.info(f'====> Fixture: Delete user (id={user["id"]}) for test')
        api_client.users.delete_user(user['id'])
    logger.info('====> Fixture setup exit')


@pytest.fixture
def setup_post_by_db(request, db_connection):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup posts by db started')
    posts_list = []
    num_entities = request.param if hasattr(request, 'param') else 1
    for _ in range(num_entities):
        logger.info('====> Fixture: Try create post for test by sql')
        post_db_client = PostDbClient(db_connection)
        post = post_db_client.create_post_in_db()
        logger.info(f'====> Fixture: Successful create post by sql (id={post["id"]}) for test.')
        posts_list.append(post)

    yield posts_list[0] if num_entities == 1 else posts_list

    for post in posts_list:
        logger.info(f'====> Fixture: Delete post by sql (id={post["id"]}) for test')
        post_db_client.delete_post_by_id_db(post['id'])
    logger.info('====> Fixture setup exit')


@pytest.fixture
def setup_user_by_db(request, db_connection):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture setup started')
    users_list = []
    num_entities = request.param if hasattr(request, 'param') else 1
    for _ in range(num_entities):
        logger.info('====> Fixture: Try create user for test by sql')
        user_db_client = UserDbClient(db_connection)
        user = user_db_client.create_user_in_db()
        logger.info(f'====> Fixture: Successful create user (id={user["id"]}) for test.')
        users_list.append(user)

    yield users_list[0] if num_entities == 1 else users_list

    for user in users_list:
        logger.info(f'====> Fixture: Delete user (id={user["id"]}) for test')
        user_db_client.delete_user_by_id_db(user['id'])
    logger.info('====> Fixture setup exit')
