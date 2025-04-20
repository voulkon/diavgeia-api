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
        base_url = client.build_url(ORGANIZATIONS)
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
        assert result.model_dump() == expected_response


@pytest.mark.integration
@pytest.mark.parametrize("params, expected_response_fixture", ORG_TEST_CASES)
# @pytest.mark.skipif("not config.getoption('--live')", reason="Needs --live flag to run")
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
