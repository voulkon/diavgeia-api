from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import DICTIONARIES

HERE = Path(__file__).parent


@pytest.fixture
def uid() -> str:
    return "FEKTYPES"


@pytest.fixture
def all_dictionaries_expected_response():
    return load_json_fixture(HERE, "dictionaries_list.json")


@pytest.fixture
def one_dictionarys_name():
    return "FEKTYPES"


@pytest.fixture
def one_dictionarys_dictionary(one_dictionarys_name):
    specific_jsons_path = f"{one_dictionarys_name}.json"
    return load_json_fixture(HERE, specific_jsons_path)


# -------- call helper fixture --------


@pytest.fixture
def all_dictionaries_result(
    client,
    all_dictionaries_expected_response,
    live,
):
    if not live:
        # Use the context manager only when mocking
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(DICTIONARIES),
                json=all_dictionaries_expected_response,
                status=200,
            )
            result = client.get_dictionaries()
    else:
        # If live, make the call outside the responses context
        result = client.get_dictionaries()
    return result


@pytest.fixture
def specific_dictionarys_result(
    client,
    uid,
    one_dictionarys_dictionary,
    live,
):
    """
    Calls client.get_dictionary(uid) once and returns its result.

    •  If NOT live: stubs the HTTP call with responses
    •  If live: hits the real API (no stub)
    """
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(DICTIONARIES, uid),
                json=one_dictionarys_dictionary,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_dictionary(uid)
    else:
        # If live, make the call outside the responses context
        result = client.get_dictionary(uid)

    return result
