import asyncpg

from app.log import logger_factory
from app.settings import cfg

logger = logger_factory.bind()
dsn = f"postgres://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.name}"


class Database:
    """Database class to handle connection pool, queries and shutdown."""

    async def connect(self):
        logger.info("Starting db connection.")
        self.connection_pool = await asyncpg.create_pool(
            dsn=dsn,
            min_size=1,
        )

    async def disconnect(self):
        logger.info("Closing db connection.")
        await self.connection_pool.close()

    async def execute(self, query: str, args: tuple):
        async with self.connection_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(query, *args)

        return result

    async def fetch(self, query: str):
        async with self.connection_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(query)

        return result

    async def fetchval(self, query: str):
        async with self.connection_pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchval(query)

        return result


db_pool = Database()
