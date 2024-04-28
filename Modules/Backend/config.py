import os

from dotenv import load_dotenv


load_dotenv()


class DBConfig:

    @staticmethod
    async def get_db_config() -> str:
        database = os.environ.get('DB_DATABASE')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT')

        url = f'postgres://{user}:{password}@{host}:{port}/{database}'

        return url

    