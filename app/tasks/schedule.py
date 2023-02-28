from app.repositories.postgres import website_repo
from app.scheduler import schedule_interval_task
from app.tasks.check_web import check_web_site


async def schedule_http_checks():
    """Schedule checks for underlying scheduler."""

    sites_to_monitor = await website_repo.get_list()

    for site in sites_to_monitor:
        if site.is_valid():
            schedule_interval_task(
                func=check_web_site,
                interval=site.interval,
                args=(site.url, site.id, site.regexp),
            )
