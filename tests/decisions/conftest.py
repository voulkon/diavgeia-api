from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import DECISIONS

HERE = Path(__file__).parent


@pytest.fixture
def decisions_uid() -> str:
    return "Ψ11446ΜΓΨ7-ΠΚΛ"


@pytest.fixture
def decisions_version_id() -> str:
    return "1f4c7ef1-ec60-460e-84d2-a8929d70adc4"


@pytest.fixture
def one_dictionarys_fixtures_file_name():
    return "one_decisions_details"


@pytest.fixture
def one_decisions_expected_response(one_dictionarys_fixtures_file_name):
    return load_json_fixture(HERE, f"{one_dictionarys_fixtures_file_name}.json")


@pytest.fixture
def one_decisions_fetched_result(
    client,
    decisions_uid,
    one_decisions_expected_response,
    live,
):
    """
    Calls client.get_a_decision(decisions_uid) once and returns its result.

    •  If NOT live: stubs the HTTP call with responses
    •  If live: hits the real API (no stub)
    """
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client.build_url(DECISIONS, decisions_uid),
                json=one_decisions_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_a_decision(decisions_uid)
    else:
        # If live, make the call outside the responses context
        result = client.get_a_decision(decisions_uid)

    return result


@pytest.fixture
def one_decisions_version_fetched_result(
    client,
    decisions_version_id,
    one_decisions_expected_response,
    live,
):
    """
    Calls client.get_a_decisions_specific_version(decisions_uid) once and returns its result.

    •  If NOT live: stubs the HTTP call with responses
    •  If live: hits the real API (no stub)
    """
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client.build_url(DECISIONS, "v", decisions_version_id),
                json=one_decisions_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_a_decisions_specific_version(decisions_version_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_a_decisions_specific_version(decisions_version_id)

    return result
