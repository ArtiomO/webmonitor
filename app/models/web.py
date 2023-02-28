import re
from dataclasses import dataclass
from datetime import datetime

from app.log import logger_factory

INTERVAL_MAX = 300
INTERVAL_MIN = 5

logger = logger_factory.bind()


@dataclass
class CheckResult:
    """Model for web_check_results table."""

    request_timestamp: datetime
    response_time: int
    http_status_code: int
    regexp_valid: bool
    website_id: int

    def to_db(self):
        return (
            self.request_timestamp,
            self.response_time,
            self.http_status_code,
            self.regexp_valid,
            self.website_id,
        )


@dataclass
class WebSite:
    """Model for websites table."""

    id: int
    url: str
    interval: int
    regexp: str
    created_at: datetime

    def is_valid(self):
        """Main validation function."""

        return (
            self.validate_regex() and self.validate_interval() and self.validate_url()
        )

    def validate_regex(self):
        """Validate regex field."""

        try:
            re.compile(self.regexp)
            return True
        except re.error:
            logger.warning("Invalid site regex.", url=self.url)
            return False

    def validate_interval(self):
        """Validate interval field."""

        if INTERVAL_MIN <= self.interval <= INTERVAL_MAX:
            return True
        else:
            logger.warning(
                f"Invalid site interval. Please provide between {INTERVAL_MIN} and {INTERVAL_MAX}.",
                url=self.url,
            )
            return False

    def validate_url(self):
        """Validate url field."""

        if self.url.startswith("https://") or self.url.startswith("http://"):
            return True
        else:
            logger.warning(
                "Invalid site url.",
                url=self.url,
            )
            return False
