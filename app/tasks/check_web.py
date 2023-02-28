import re
from datetime import datetime

from app.clients.http import HttpClientConnectionError, http_client
from app.log import logger_factory
from app.models.web import CheckResult
from app.repositories.postgres import check_result_repo

logger = logger_factory.bind()


async def check_web_site(url: str, web_site_id: int, regexp: str):
    """Check website main function."""

    timestamp = datetime.utcnow()

    try:
        status, response, latency = await http_client.request(url=url, method="get")
    except HttpClientConnectionError:
        logger.warning("Connection timeout", url=url)
        return

    regex_result = check_string(regexp, response)

    if not regex_result:
        logger.warning("Regex doesn't matched with response", url=url)

    result = CheckResult(
        request_timestamp=timestamp,
        response_time=latency,
        http_status_code=status,
        regexp_valid=regex_result,
        website_id=web_site_id,
    )

    await check_result_repo.save(result)


def check_string(regex: str, string: str) -> bool:
    """Check string regex."""

    if re.match(regex, string):
        return True
    else:
        return False
