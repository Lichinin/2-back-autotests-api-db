from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


class Paths:
    LOG_DIR = Path(__file__).parent / 'log'


class APiRoutes:

    BASE_URL = os.getenv('BASE_URL')
    API_VER = '/wp-json/wp/v2'
