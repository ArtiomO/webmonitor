import typing as tp

from app.db.pg import db_pool
from app.models.web import CheckResult, WebSite
from app.repositories.base import AbstractRepository

check_result_save_query = """
INSERT INTO web_check_results (
request_timestamp, 
response_time, 
http_status_code, 
regexp_valid, 
website_id
)
VALUES ($1, $2, $3, $4, $5);
"""

website_save_query = """
INSERT INTO website 
VALUES ($1, $2, $3, $4);
"""


class CheckResultPostgreRepository(AbstractRepository):
    """Repository for postgres web_check_results table."""

    async def save(self, instance: CheckResult):
        """Save instance to db."""
        saved_instance = db_pool.fetchval(check_result_save_query, (instance.to_db()))
        await db_pool.fetchval(check_result_save_query, (instance.to_db()))

    async def get_list(self) -> tp.List[CheckResult]:
        """Retrieve list of CheckResult instances."""

        result = await db_pool.fetch("select * from web_check_results")
        return [CheckResult(**dict(row)) for row in result]


class WebSitePostgreRepository(AbstractRepository):
    """Repository for postgres websites table."""

    async def save(self, instance: CheckResult):
        """Save instance to db."""

        await db_pool.execute(check_result_save_query, *instance.to_db())

    async def get_list(self) -> tp.List[WebSite]:
        """Retrieve list of WebSite instances."""

        result = await db_pool.fetch("select * from websites")
        return [WebSite(**dict(row)) for row in result]


check_result_repo = CheckResultPostgreRepository()
website_repo = WebSitePostgreRepository()
