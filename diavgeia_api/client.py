import requests
from requests.auth import HTTPBasicAuth
from .exceptions import DiavgeiaAPIError, DiavgeiaNetworkError
from ._config import (
    BASE_URL,
    DEFAULT_HEADERS,
    TYPES,
    DECISIONS,
    ORGANIZATIONS,
    SEARCH,
    SIGNERS,
    POSITIONS,
    DICTIONARIES,
    UNITS,
)
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from .models.dictionaries import DictionariesListResponse, DictionaryValuesResponse
from .models.decisions import (
    Decision,
    DecisionVersions,
)
from .models.organizations import (
    OrganizationsResponse,
    OrganizationStatus,
    Organization,
    UnitsResponse,
    SignersResponse,
    PositionsResponse,
)
from loguru import logger

T = TypeVar("T", bound=BaseModel)


class DiavgeiaClient:
    """
    Parameters
    ----------
    username, password : optional
        If both are provided the client sends Basic‑Auth on every request.
    base_url : str
        Override only for testing or if the service changes host.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        base_url: str = BASE_URL,
        session: Optional[requests.Session] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        if username and password:
            # requests will add the correct `Authorization: Basic …` header
            self.session.auth = HTTPBasicAuth(username, password)
        elif username or password:
            raise ValueError("Both username and password must be provided, or neither.")

    def build_url(self, *parts: str) -> str:
        return "/".join([self.base_url.rstrip("/")] + [p.strip("/") for p in parts])

    def _get_and_parse(
        self,
        model: Type[T],
        *url_parts: str,
        params: Optional[dict] = None,
    ) -> T:
        raw = self._request("GET", self.build_url(*url_parts), params=params)
        return model(**raw)

    # main low‑level request wrapper
    def _request(self, method: str, url: str, **kwargs):
        try:
            resp = self.session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise DiavgeiaNetworkError(f"Network error: {exc}") from exc

        if not resp.ok:
            raise DiavgeiaAPIError(resp.status_code, resp.text)
        return resp.json()

    def _get_and_parse(self, model: Type[T], *path_parts: str, params=None) -> T:
        raw = self._request("GET", self.build_url(*path_parts), params=params)
        # You can insert logging/debugging here
        # logger.debug(f"Raw response for {'/'.join(path_parts)}: {raw}")
        return model(**raw)

    def get_dictionaries(self) -> DictionariesListResponse:
        """Return the list of available dictionaries."""
        return self._get_and_parse(DictionariesListResponse, DICTIONARIES)

    def get_dictionary(self, uid: str) -> DictionaryValuesResponse:
        """Return all items for a specific dictionary."""
        return self._get_and_parse(DictionaryValuesResponse, DICTIONARIES, uid)

    def get_a_decision(self, uid: str) -> Decision:
        """Return a specific decision's details."""
        return self._get_and_parse(Decision, DECISIONS, uid)

    def get_a_decisions_specific_version(self, versionId: str) -> Decision:
        """Returns details of a specific version of a decision."""
        return self._get_and_parse(Decision, DECISIONS, "v", versionId)

    def get_a_decisions_version_log(self, decisions_uid: str) -> DecisionVersions:
        """Returns details of a specific version of a decision."""
        return self._get_and_parse(
            DecisionVersions, DECISIONS, decisions_uid, "versionlog"
        )

    def get_organizations(
        self,
        status: Optional[OrganizationStatus] = None,
        category: Optional[str] = None,
    ) -> OrganizationsResponse:
        """
        Returns a list of registered organizations.

        Parameters
        ----------
        status : OrganizationStatus, optional
            Filter by organization status (active, inactive, pending). Defaults to active if not provided by the API.
        category : str, optional
            Filter by organization category code (from ORG_CATEGORY dictionary).
        """
        params = {}
        if status:
            params["status"] = status.value  # Use the enum's value
        if category:
            params["category"] = category

        # Pass params only if it's not empty, otherwise pass None
        return self._get_and_parse(
            OrganizationsResponse, ORGANIZATIONS, params=params if params else None
        )

    def get_organization(
        self,
        organization_id: str,
    ) -> Organization:
        """
        Returns details of a specific organization.

        Parameters
        ----------
        organization_id : str
            The unique identifier of the organization.
        """
        return self._get_and_parse(Organization, ORGANIZATIONS, organization_id)

    def get_organization_units(
        self,
        organization_id: str,
    ) -> UnitsResponse:
        """
        Returns units of a specific organization.

        Parameters
        ----------
        organization_id : str
            The unique identifier of the organization.
        """
        return self._get_and_parse(
            UnitsResponse, ORGANIZATIONS, organization_id, "units"
        )

    def get_organization_signers(
        self,
        organization_id: str,
    ) -> SignersResponse:
        """
        Returns signers of a specific organization.

        Parameters
        ----------
        organization_id : str
            The unique identifier of the organization.
        """
        return self._get_and_parse(
            SignersResponse, ORGANIZATIONS, organization_id, "signers"
        )

    def get_organization_positions(
        self,
        organization_id: str,
    ) -> PositionsResponse:
        """
        Returns positions of a specific organization.

        Parameters
        ----------
        organization_id : str
            The unique identifier of the organization.
        """
        return self._get_and_parse(
            PositionsResponse, ORGANIZATIONS, organization_id, "positions"
        )
