import typing as tp

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


def schedule_interval_task(func: tp.Callable, interval: int, args: tp.Tuple):
    """Wraps APScheduler library. Add job."""

    scheduler.add_job(func, "interval", seconds=interval, args=args, max_instances=10)


def start_scheduler():
    """Wraps APScheduler library. Start scheduler."""

    scheduler.start()
