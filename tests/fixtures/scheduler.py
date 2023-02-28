import pytest


@pytest.fixture()
def mock_scheduler(mocker):
    """Mock scheduler."""

    return mocker.patch("app.tasks.schedule.schedule_interval_task")
