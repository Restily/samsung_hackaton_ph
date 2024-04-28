import json
from typing import Iterable, Optional
from asyncpg import create_pool


from config import DBConfig


class DBWorker:

    pool = None

    @classmethod
    async def get_pool(cls):
        if not cls.pool:
            db_config_url = await DBConfig.get_db_config()

            cls.pool = await create_pool(db_config_url)

        return cls.pool

    @classmethod
    async def fetch(cls, query: str, *params) -> list[dict]:
        pool = await cls.get_pool()

        async with pool.acquire() as conn:
            await conn.set_type_codec(
                'jsonb',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )

            rows = [dict(row) for row in await conn.fetch(query, *params)]

        return rows

    @classmethod
    async def execute(cls, query: str, *values):
        pool = await cls.get_pool()

        async with pool.acquire() as conn:
            await conn.execute(query, *values)

    @classmethod
    async def close_pool(cls):
        pool = await cls.get_pool()

        await pool.close()

    @classmethod
    async def start_database(cls):
        with open('data/tables.sql', 'r') as f:
            create_sql = f.read()

        await cls.execute(create_sql)
