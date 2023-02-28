import random
from datetime import datetime

import pytest

from app.models.web import WebSite


@pytest.fixture()
def website_model_factory():
    def factory(interval: int, url: str, regex: str) -> WebSite:
        instance = WebSite(
            id=random.randint(1, 100),
            interval=interval,
            url=url,
            regexp=regex,
            created_at=datetime.utcnow(),
        )
        return instance

    return factory
