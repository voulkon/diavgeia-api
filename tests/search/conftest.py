from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import SEARCH

HERE = Path(__file__).parent


@pytest.fixture
def simple_search_criteria() -> str:
    simple_search_criteria = {"from_date": "2025-04-20", "to_date": "2025-04-21"}
    return simple_search_criteria


@pytest.fixture
def simple_searches_expected_response():
    return load_json_fixture(HERE, "simple_query_search_result.json")


@pytest.fixture
def simple_searches_fetched_result(
    client,
    simple_search_criteria,
    simple_searches_expected_response,
    live,
):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                # TODO: Not sure if the _build_url(SEARCH, **simple_search_criteria) will work
                # Gotta check how it gets passed up to this point:
                # self._build_url(*path_parts)
                url=client._build_url(SEARCH, **simple_search_criteria),
                json=simple_searches_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.search_decisions(**simple_search_criteria)
    else:
        # If live, make the call outside the responses context
        result = client.search_decisions(**simple_search_criteria)

    return result


@pytest.fixture
def complex_search_criteria() -> str:
    complex_search_criteria = {
        "org": "nosokomeio_limnou;51611",
        # {
        #     "uid": "99221771",
        #     "label": "ΓΕΝΙΚΟ ΝΟΣΟΚΟΜΕΙΟ - ΚΕΝΤΡΟ ΥΓΕΙΑΣ ΛΗΜΝΟΥ",
        #     "abbreviation": null,
        #     "latinName": "nosokomeio_limnou",
        #     "status": "active",
        #     "category": "OTHERTYPE",
        #     "vatNumber": "800187255",
        #     "fekNumber": "0",
        #     "fekIssue": "",
        #     "fekYear": "0",
        #     "odeManagerEmail": "limnoshospital@gmail.com",
        #     "website": "",
        #     "supervisorId": "100010899",
        #     "supervisorLabel": "ΥΠΟΥΡΓΕΙΟ ΥΓΕΙΑΣ ΚΑΙ ΚΟΙΝΩΝΙΚΩΝ ΑΣΦΑΛΙΣΕΩΝ",
        #     "organizationDomains": []
        # }
        # {
        #     "uid": "51611",
        #     "label": "ΔΗΜΟΤΙΚΟ ΛΙΜΕΝΙΚΟ ΤΑΜΕΙΟ ΛΗΜΝΟΥ",
        #     "abbreviation": null,
        #     "latinName": "dlt_limnou",
        #     "status": "active",
        #     "category": "NPDD",
        #     "vatNumber": "800186744",
        #     "fekNumber": "0",
        #     "fekIssue": "",
        #     "fekYear": "0",
        #     "odeManagerEmail": "",
        #     "website": "http://dmirinas@yahoo.gr",
        #     "supervisorId": "6174",
        #     "supervisorLabel": "ΔΗΜΟΣ ΛΗΜΝΟΥ",
        #     "organizationDomains": []
        # },
        # "type": "2.4.2;2.4.4",
        "from_date": "2023-04-20",
        "to_date": "2025-04-21",
        "from_issue_date": "2023-04-20",
        "to_issue_date": "2025-04-21",
    }
    return complex_search_criteria


@pytest.fixture
def complex_searches_expected_response():
    return load_json_fixture(HERE, "complex_search_result.json")


@pytest.fixture
def complex_searches_fetched_result(
    client,
    complex_search_criteria,
    complex_searches_expected_response,
    live,
):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                # TODO: Not sure if the _build_url(SEARCH, **simple_search_criteria) will work
                # Gotta check how it gets passed up to this point:
                # self._build_url(*path_parts)
                url=client._build_url(SEARCH, **complex_search_criteria),
                json=complex_searches_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.search_decisions(**complex_search_criteria)
    else:
        # If live, make the call outside the responses context
        result = client.search_decisions(**complex_search_criteria)

    return result
