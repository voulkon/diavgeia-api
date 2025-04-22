import pytest
from diavgeia_api.models.organizations import OrganizationStatus, OrganizationsResponse
from diavgeia_api._config import ORGANIZATIONS
import responses
import urllib.parse


ORG_TEST_CASES = [
    pytest.param(
        {"category": "MINISTRY"},
        "organizations_of_ministry_expected_response",
        id="category_ministry",
    ),
    pytest.param(
        {"status": OrganizationStatus.ACTIVE},
        "organizations_active_expected_response",
        id="status_active",
    ),
    pytest.param(
        {"category": "MINISTRY", "status": OrganizationStatus.INACTIVE},
        "organizations_inactive_ministry_expected_response",
        id="category_ministry_status_inactive",
    ),
    pytest.param(
        {},
        "organizations_no_params_expected_response",
        id="no_params_default",
    ),
]


@pytest.mark.parametrize("params, expected_response_fixture", ORG_TEST_CASES)
def test_get_organizations_mocked(client, params, expected_response_fixture, request):
    """Tests get_organizations with mocked responses."""
    expected_response = request.getfixturevalue(expected_response_fixture)

    with responses.RequestsMock() as rs:
        # Build URL based on params
        base_url = client._build_url(ORGANIZATIONS)
        expected_url = base_url
        if params:
            encoded_params = {
                k: v.value if isinstance(v, OrganizationStatus) else v
                for k, v in params.items()
            }
            expected_url += "?" + urllib.parse.urlencode(encoded_params)

        rs.add(
            method=responses.GET,
            url=expected_url,
            json=expected_response,
            status=200,
            # match_querystring=False,
        )

        # Call the client method
        result = client.get_organizations(**params)

        # Assertions for mocked response
        assert isinstance(result, OrganizationsResponse)
        orgs_in_result = [org.uid for org in result.organizations]
        orgs_in_expected = [org["uid"] for org in expected_response["organizations"]]
        assert len(result.organizations) == len(expected_response["organizations"])
        assert all(org in orgs_in_expected for org in orgs_in_result)
        assert all(org in orgs_in_result for org in orgs_in_expected)


@pytest.mark.integration
@pytest.mark.parametrize("params, expected_response_fixture", ORG_TEST_CASES)
@pytest.mark.skipif("not config.getoption('--live')", reason="Needs --live flag to run")
def test_get_organizations_live(client, params, expected_response_fixture):
    """Tests get_organizations with live API calls."""
    # Call the client method against the live API
    result = client.get_organizations(**params)

    # Basic validation
    assert isinstance(result, OrganizationsResponse)
    assert isinstance(result.organizations, list)

    # Parameter-specific checks
    if "status" in params:
        if result.organizations:
            assert all(org.status == params["status"] for org in result.organizations)

    if "category" in params:
        if result.organizations:
            assert all(
                org.category == params["category"] for org in result.organizations
            )

    # Verify we got results when we should
    if not params or params.get("status") == OrganizationStatus.ACTIVE:
        assert len(result.organizations) > 0


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_get_organization(an_org_expected_result, a_dummy_org_id):
    assert an_org_expected_result.uid == a_dummy_org_id
    # assert an_org_expected_result.label == "ΔΗΜΟΣ ΛΗΜΝΟΥ"
    # assert an_org_expected_result.category == "MUNICIPALITY"


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_get_organizations_units(an_orgs_units_expected_result, a_dummy_org_id):
    assert an_orgs_units_expected_result.units[0].uid == "93542"
    # assert an_org_expected_result.label == "ΔΗΜΟΣ ΛΗΜΝΟΥ"
    # assert an_org_expected_result.category == "MUNICIPALITY"


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_get_organizations_signers(an_orgs_signers_expected_result, a_dummy_org_id):
    ...
    assert an_orgs_signers_expected_result.signers[0].organizationId == a_dummy_org_id


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_get_organizations_positions(an_orgs_positions_expected_result, a_dummy_org_id):

    label_to_look_for = "Δήμαρχος"
    label_exists_in_response = any(
        label_to_look_for.lower() in position.label.lower()
        for position in an_orgs_positions_expected_result.positions
    )
    assert (
        label_exists_in_response
    ), f"Label '{label_to_look_for}' not found in positions."
