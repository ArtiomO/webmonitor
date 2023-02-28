import pytest


@pytest.mark.parametrize(
    ("url", "interval", "regex"),
    [("https://google.com", 5, "{}"), ("http://amazon.com", 5, "{}")],
)
def test_website_is_valid(website_model_factory, url: str, interval: int, regex: str):
    instance = website_model_factory(url=url, interval=interval, regex=regex)
    assert instance.is_valid()


@pytest.mark.parametrize(
    ("url", "interval", "regex", "log_str"),
    [
        ("https://google.com", 0, "{}", "Invalid site interval."),
        ("https://amazon.com", 5, "****$$$", "Invalid site regex."),
        ("test://amazon.com", 5, "{}", "Invalid site url."),
        ("https://amazon.com", 301, "{}", "Invalid site interval."),
    ],
)
def test_website_validation_exception_logging(
    website_model_factory, caplog, url: str, interval: int, regex: str, log_str: str
):
    instance = website_model_factory(url=url, interval=interval, regex=regex)
    instance.is_valid()
    assert log_str in caplog.text
