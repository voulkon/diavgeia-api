from pathlib import Path
import pytest
import responses
from tests.utils import load_json_fixture
from diavgeia_api._config import ORGANIZATIONS, SIGNERS

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
def organizations_no_params_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "organizations_no_params.json")


@pytest.fixture
def a_dummy_org_id():
    """Returns a dummy organization ID for testing."""
    #     {
    #     "uid": "6174",
    #     "label": "ΔΗΜΟΣ ΛΗΜΝΟΥ",
    #     "abbreviation": null,
    #     "latinName": "dimos_limnou",
    #     "status": "active",
    #     "category": "MUNICIPALITY",
    #     "vatNumber": "800189144",
    #     "fekNumber": "87",
    #     "fekIssue": "fektype_A",
    #     "fekYear": "2010",
    #     "odeManagerEmail": "dlimnou@gmail.com",
    #     "website": "http://www.limnos.gov.gr",
    #     "supervisorId": "5003",
    #     "supervisorLabel": "ΠΕΡΙΦΕΡΕΙΑ ΒΟΡΕΙΟΥ ΑΙΓΑΙΟΥ",
    #     "organizationDomains": []
    # },
    return "6174"


@pytest.fixture
def an_orgs_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "an_org.json")


@pytest.fixture
def an_orgs_units_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "an_orgs_units.json")


@pytest.fixture
def an_orgs_signers_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "an_orgs_signers.json")


@pytest.fixture
def an_orgs_positions_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "an_orgs_positions.json")


@pytest.fixture
def specific_signers_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "specific_signer.json")


@pytest.fixture
def signer_no_position_id_expected_response():
    """Expected response for default call (no params)"""

    return load_json_fixture(HERE, "signer_without_poisitionid.json")


@pytest.fixture
def signers_without_position_id_unique_id() -> str:
    """Expected response for default call (no params)"""

    return "100058444"


@pytest.fixture
def specific_signers_unique_id() -> str:
    """Expected response for default call (no params)"""

    return "100047871"


@pytest.fixture
def an_org_expected_result(client, an_orgs_expected_response, a_dummy_org_id, live):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(ORGANIZATIONS, a_dummy_org_id),
                json=an_orgs_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_organization(organization_id=a_dummy_org_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_organization(organization_id=a_dummy_org_id)

    return result


@pytest.fixture
def an_orgs_units_expected_result(
    client, an_orgs_units_expected_response, a_dummy_org_id, live
):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(ORGANIZATIONS, a_dummy_org_id, "units"),
                json=an_orgs_units_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_organization_units(organization_id=a_dummy_org_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_organization_units(organization_id=a_dummy_org_id)

    return result


@pytest.fixture
def an_orgs_signers_expected_result(
    client, an_orgs_signers_expected_response, a_dummy_org_id, live
):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(ORGANIZATIONS, a_dummy_org_id, "signers"),
                json=an_orgs_signers_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_organization_signers(organization_id=a_dummy_org_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_organization_signers(organization_id=a_dummy_org_id)

    return result


@pytest.fixture
def an_orgs_positions_expected_result(
    client, an_orgs_positions_expected_response, a_dummy_org_id, live
):
    ...
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(ORGANIZATIONS, a_dummy_org_id, "positions"),
                json=an_orgs_positions_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_organization_positions(organization_id=a_dummy_org_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_organization_positions(organization_id=a_dummy_org_id)

    return result


@pytest.fixture
def a_specific_signers_expected_result(
    client, specific_signers_expected_response, specific_signers_unique_id, live
):
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(SIGNERS, specific_signers_unique_id),
                json=specific_signers_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_specific_signer(signer_id=specific_signers_unique_id)
    else:
        # If live, make the call outside the responses context
        result = client.get_specific_signer(signer_id=specific_signers_unique_id)

    return result


@pytest.fixture
def signers_without_position_id_expected_result(
    client,
    signer_no_position_id_expected_response,
    signers_without_position_id_unique_id,
    live,
):
    if not live:
        with responses.RequestsMock() as rs:
            rs.add(
                method=responses.GET,
                url=client._build_url(SIGNERS, signers_without_position_id_unique_id),
                json=signer_no_position_id_expected_response,
                status=200,
            )
            # The call must happen *inside* the context manager when mocking
            result = client.get_specific_signer(
                signer_id=signers_without_position_id_unique_id
            )
    else:
        # If live, make the call outside the responses context
        result = client.get_specific_signer(
            signer_id=signers_without_position_id_unique_id
        )

    return result
