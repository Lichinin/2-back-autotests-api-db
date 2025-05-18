import logging
from logging.handlers import RotatingFileHandler

import pytest

from api_client.api_client import ApiClient
from config import Paths


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


@pytest.fixture(scope='function')
def api_client(request):
    logger = logging.getLogger(f'fixture.{request.fixturename}')
    logger.info('====> Fixture ApiClient started')
    client = ApiClient()

    yield client

    logger.info('====> Fixture ApiClient teardown')
