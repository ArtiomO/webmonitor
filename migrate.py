import asyncio

from app.db.pg import db_pool
from app.migrations.initial_migration import initial_migration_script
from asyncpg.exceptions import DuplicateTableError
from app.log import logger_factory

logger = logger_factory.bind()


async def execute_migrations():
    await db_pool.connect()
    try:
        await db_pool.execute(initial_migration_script, ())
    except DuplicateTableError:
        logger.error("Duplicate table error")
    await db_pool.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_migrations())
