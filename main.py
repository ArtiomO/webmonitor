import asyncio

from app.db.pg import db_pool
from app.scheduler import start_scheduler
from app.settings import cfg
from app.tasks.schedule import schedule_http_checks

dsn = f"postgres://{cfg.user}:{cfg.password}@{cfg.host}:{cfg.port}/{cfg.name}"


async def on_startup():
    """On start tasks."""

    await db_pool.connect()
    loop.create_task(schedule_http_checks())
    start_scheduler()


async def on_shutdown():
    """On shutdown tasks."""

    await db_pool.disconnect()


if __name__ == "__main__":
    """Retrieve asyncio loop. Do initial preparations. Shutdown on signals."""
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(on_startup())
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        loop.run_until_complete(on_shutdown())
        pass
