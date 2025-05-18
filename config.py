from pathlib import Path


class Paths:
    LOG_DIR = Path(__file__).parent / 'log'


class APiRoutes:

    BASE_URL = 'http://localhost:8000'
    API_VER = '/wp-json/wp/v2'
