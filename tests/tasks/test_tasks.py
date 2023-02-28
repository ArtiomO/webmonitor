import pytest

from app.tasks.check_web import check_string, check_web_site


@pytest.mark.parametrize(
    ("string", "is_valid"),
    [("<input value = '>'>", True), ("br/>", False)],
)
def test_check_string(string: str, is_valid: bool):
    regex = r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>"

    if is_valid:
        assert check_string(regex, string)
    else:
        assert not check_string(regex, string)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("url", "web_site_id", "regexp", "log_str"),
    [("https://test.com", 1, "{}", "Connection timeout")],
)
async def test_check_website_exception_logging(
    mock_http_exception_client,
    caplog,
    url: str,
    web_site_id: int,
    regexp: str,
    log_str: str,
):
    await check_web_site(url, web_site_id, regexp)
    assert log_str in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("url", "web_site_id", "regexp", "status", "text", "latency", "log_str"),
    [
        (
            "https://test.com",
            1,
            "{}",
            1,
            "test",
            100,
            "Regex doesn't matched with response",
        )
    ],
)
async def test_check_website_regex_logging(
    mock_http_client,
    mock_check_result_repository,
    caplog,
    url: str,
    web_site_id: int,
    regexp: str,
    status: str,
    text: str,
    latency: int,
    log_str: str,
):
    mock_http_client(status=status, text=text, latency=latency)
    mock_check_result_repository(check_results=None)
    await check_web_site(url, web_site_id, regexp)
    assert log_str in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("url", "web_site_id", "regexp", "status", "text", "latency", "regexp_valid"),
    [
        ("https://test.com", 1, "{}", 1, "test", 100, False),
        (
            "https://test.com",
            1,
            r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>",
            1,
            "<input value = '>'>",
            100,
            True,
        ),
    ],
)
async def test_check_website_save(
    mock_http_client,
    mock_check_result_repository,
    caplog,
    url: str,
    web_site_id: int,
    regexp: str,
    status: str,
    text: str,
    latency: int,
    regexp_valid: bool,
):
    mock_http_client(status=status, text=text, latency=latency)
    repo_mock = mock_check_result_repository(check_results=None)
    await check_web_site(url, web_site_id, regexp)
    called_with = repo_mock.save.call_args.args
    assert called_with[0].http_status_code == status
    assert called_with[0].regexp_valid == regexp_valid
