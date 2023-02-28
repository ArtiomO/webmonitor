import pytest

from app.tasks.schedule import schedule_http_checks


@pytest.mark.asyncio
async def test_schedule_http_checks(
    mock_web_site_repository, website_model_factory, mock_scheduler
):
    website = website_model_factory(interval=5, url="http://", regex="{}")
    mock_web_site_repository(websites=[website])
    await schedule_http_checks()
    mock_scheduler.assert_called_once()
