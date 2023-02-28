import pytest

from app.clients.http import HttpClientConnectionError


class DummyHttpClient:
    """Dummy http client."""

    def __init__(self, status: int, text: str, latency: int):
        self.response = (status, text, latency)

    async def request(self, url: str, method: str) -> (int, dict):
        return self.response


class DummyExceptionHttpClient:
    """Dummy http client with connection exception."""

    async def request(self, url: str, method: str) -> (int, dict):
        raise HttpClientConnectionError


@pytest.fixture()
def mock_http_client(mocker):
    """Mock http client."""

    def factory(status: int, text: str, latency: int):
        client_instance = DummyHttpClient(status=status, text=text, latency=latency)
        mocker.patch("app.tasks.check_web.http_client", client_instance)

    return factory


@pytest.fixture()
def mock_http_exception_client(mocker):
    """Mock http client returning exception."""

    client_instance = DummyExceptionHttpClient()
    return mocker.patch("app.tasks.check_web.http_client", client_instance)
