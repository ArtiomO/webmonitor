import typing as tp
from unittest.mock import AsyncMock

import pytest

from app.models.web import CheckResult, WebSite


class DummyWebSiteRepository:
    """Dummy website repository."""

    def __init__(self, websites: tp.List[WebSite]):
        self.websites = websites

    async def save(self, instance: CheckResult):
        pass

    async def get_list(self) -> tp.List[WebSite]:
        return self.websites


class DummyCheckResultRepository:
    """Dummy check result repository."""

    def __init__(self, check_results: tp.List[CheckResult]):
        self.check_results = check_results

    async def save(self, instance: CheckResult):
        pass

    async def get_list(self) -> tp.List[CheckResult]:
        return self.check_results


@pytest.fixture()
def mock_web_site_repository(mocker):
    """Mock website db repository calls."""

    def factory(websites: tp.List[WebSite]):
        repo_instance = DummyWebSiteRepository(websites=websites)
        repo_instance.save = AsyncMock(return_value=websites)
        return mocker.patch("app.tasks.schedule.website_repo", repo_instance)

    return factory


@pytest.fixture()
def mock_check_result_repository(mocker):
    """Mock website db repository calls."""

    def factory(check_results: tp.List[CheckResult]):
        repo_instance = DummyCheckResultRepository(check_results=check_results)
        repo_instance.save = AsyncMock(return_value=None)

        return mocker.patch("app.tasks.check_web.check_result_repo", repo_instance)

    return factory
