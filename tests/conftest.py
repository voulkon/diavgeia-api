import pytest
from diavgeia_api.client import DiavgeiaClient


def pytest_addoption(parser):
    parser.addoption(
        "--live",
        action="store_true",
        # default=False,
        default=True,
        help="Run integration tests with real Diavgeia API",
    )


@pytest.fixture(scope="session")
def live(request):
    """Fixture to get the value of the --live command line option."""
    return request.config.getoption("--live")


@pytest.fixture
def client() -> DiavgeiaClient:
    """
    Fresh client instance for every test.

    •  If you need auth in some tests, parametrize or override in a domain conftest (see notes below).
    """
    return DiavgeiaClient()  # unauthenticated by default
