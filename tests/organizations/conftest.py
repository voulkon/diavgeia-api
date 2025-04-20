from pathlib import Path
import pytest
from tests.utils import load_json_fixture

# Keep other necessary imports like responses, urllib.parse, ORGANIZATIONS if needed elsewhere

HERE = Path(__file__).parent

# --- Data Fixtures ---


@pytest.fixture
def organizations_of_ministry_expected_response():
    """Expected response for category=MINISTRY"""
    return load_json_fixture(HERE, "organizations_of_ministry.json")


@pytest.fixture
def organizations_active_expected_response():
    """Expected response for status=active"""

    return load_json_fixture(HERE, "organizations_active.json")


@pytest.fixture
def organizations_inactive_ministry_expected_response():
    """Expected response for category=MINISTRY, status=inactive"""

    return load_json_fixture(HERE, "organizations_inactive_ministry.json")


@pytest.fixture
def organizations_default_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "organizations_no_params.json")
