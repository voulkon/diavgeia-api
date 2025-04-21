from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import TYPES

# Keep other necessary imports like responses, urllib.parse, ORGANIZATIONS if needed elsewhere

HERE = Path(__file__).parent

# --- Data Fixtures ---


@pytest.fixture
def all_types_expected_response():
    """Expected response for all types"""
    return load_json_fixture(HERE, "all_types.json")


@pytest.fixture
def type_to_target():
    # {
    #         "uid": "2.4.2",
    #         "label": "ΠΡΑΞΕΙΣ ΟΙΚΟΝΟΜΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ",
    #         "parent": null,
    #         "allowedInDecisions": false
    # },
    return "2.4.6.1"


@pytest.fixture
def details_of_a_type():
    """Expected response for all types"""
    return load_json_fixture(HERE, "details_of_2_4_6_1_type.json")


@pytest.fixture
def all_types_expected_result(client, all_types_expected_response, live):

    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(
                    TYPES,
                ),
                json=all_types_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_all_types()
    else:
        # If live, make the call outside the responses context
        result = client.get_all_types()

    return result


@pytest.fixture
def details_of_a_type_result(client, details_of_a_type, type_to_target, live):

    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(TYPES, type_to_target, "details"),
                json=details_of_a_type,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_a_types_details(types_uid=type_to_target)
    else:
        # If live, make the call outside the responses context
        result = client.get_a_types_details(types_uid=type_to_target)

    return result
