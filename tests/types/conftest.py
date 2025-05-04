from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import TYPES

HERE = Path(__file__).parent

# --- Data Fixtures ---

# Define type mapping configuration
TYPE_FIXTURES = {
    "2.4.6.1": {
        "fixture_filename": "details_of_2_4_6_1_type.json",
        "label_to_look_for": "ΠΡΑΞΕΙΣ ΧΩΡΟΤΑΞΙΚΟΥ - ΠΟΛΕΟΔΟΜΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ",
    },
    "Β.6": {
        "fixture_filename": "details_of_b_6_type.json",
        "label_to_look_for": "ΠΡΟΓΡΑΜΜΑΤΙΚΗ ΣΥΜΦΩΝΙΑ ΟΙΚΟΝΟΜΙΚΗΣ ΥΠΟΣΤΗΡΙΞΗΣ",
    },
}


@pytest.fixture
def all_types_expected_response():
    """Expected response for all types"""
    return load_json_fixture(HERE, "all_types.json")


@pytest.fixture(params=list(TYPE_FIXTURES.keys()))
def type_to_target(request):
    """Provides different type IDs to test"""
    return request.param


@pytest.fixture
def details_of_a_type(type_to_target):
    """Expected response for type details based on the selected type"""
    fixture_filename = TYPE_FIXTURES[type_to_target]["fixture_filename"]
    return load_json_fixture(HERE, fixture_filename)


@pytest.fixture
def general_label_of_type_details_to_look_for(type_to_target):
    """Returns the expected label for the current type being tested"""
    return TYPE_FIXTURES[type_to_target]["label_to_look_for"]


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
