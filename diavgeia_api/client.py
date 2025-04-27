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
    WANTED_DATE_FORMAT,
)
from typing import Type, TypeVar, Optional, List, Union
from pydantic import BaseModel
from .models.dictionaries import DictionariesListResponse, DictionaryValuesResponse
from .models.decisions import Decision, DecisionVersions, DecisionStatus
from .models.organizations import (
    OrganizationsResponse,
    OrganizationStatus,
    Organization,
    UnitsResponse,
    SignersResponse,
    PositionsResponse,
)
from .models.types import TypeSummaries, TypeSummary, TypeDetails
from .models.search import SearchResponse, SortOrder
import datetime
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

        logger.debug(f"Initializing DiavgeiaClient with base_url: {self.base_url}")

        if username and password:
            # requests will add the correct `Authorization: Basic …` header
            self.session.auth = HTTPBasicAuth(username, password)
            logger.debug("Authentication configured with provided credentials")
        elif username or password:
            logger.error("Authentication error: Only one credential provided")
            raise ValueError("Both username and password must be provided, or neither.")

    def _build_url(self, *parts: str) -> str:
        url = "/".join([self.base_url.rstrip("/")] + [p.strip("/") for p in parts])
        logger.trace(f"Built URL: {url}")  # Using trace for very detailed logging
        return url

    # main low‑level request wrapper
    def _request(self, method: str, url: str, **kwargs):
        logger.debug(f"{method} request to: {url}")
        if kwargs.get("params"):
            logger.debug(f"Request parameters: {kwargs['params']}")

        try:
            resp = self.session.request(method, url, **kwargs)
            logger.debug(f"Response status: {resp.status_code}")
        except requests.RequestException as exc:
            logger.error(f"Network error during {method} request to {url}: {exc}")
            raise DiavgeiaNetworkError(f"Network error: {exc}") from exc

        if not resp.ok:
            logger.warning(f"API error: {resp.status_code} - {resp.text[:200]}")
            raise DiavgeiaAPIError(resp.status_code, resp.text)

        logger.debug(f"Successful response from {url}")
        return resp.json()

    def _get_and_parse(self, model: Type[T], *path_parts: str, params=None) -> T:
        endpoint = "/".join(path_parts)
        logger.debug(f"Fetching data from endpoint: {endpoint}")

        raw = self._request("GET", self._build_url(*path_parts), params=params)

        # Log response size for debugging
        logger.debug(f"Response size: {len(str(raw))} characters")

        # Log with a sample of the data for debugging purposes
        if isinstance(raw, dict):
            # Create a sample of keys and truncate large output
            sample = {k: v for i, (k, v) in enumerate(raw.items()) if i < 3}
            log_data = str(raw)
            if len(log_data) > 5000:
                logger.debug(
                    f"Large response truncated: {log_data[:2500]}...{log_data[-2500:]} "
                    f"(total length: {len(log_data)} characters)"
                )
            else:
                logger.debug(f"Sample response data: {sample}")
        elif isinstance(raw, list) and raw:
            logger.debug(f"Response contains a list with {len(raw)} items")

        try:
            result = model(**raw)
            logger.debug(f"Successfully parsed response into {model.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error parsing response into {model.__name__}: {e}")
            raise

    def get_dictionaries(self) -> DictionariesListResponse:
        """Return the list of available dictionaries."""
        logger.info("Fetching available dictionaries")
        return self._get_and_parse(DictionariesListResponse, DICTIONARIES)

    def get_dictionary(self, uid: str) -> DictionaryValuesResponse:
        """Return all items for a specific dictionary."""
        logger.info(f"Fetching dictionary items for: {uid}")
        return self._get_and_parse(DictionaryValuesResponse, DICTIONARIES, uid)

    def get_a_decision(self, uid: str) -> Decision:
        """Return a specific decision's details."""
        logger.info(f"Fetching decision with ADA: {uid}")
        return self._get_and_parse(Decision, DECISIONS, uid)

    def get_a_decisions_specific_version(self, versionId: str) -> Decision:
        """Returns details of a specific version of a decision."""
        logger.info(f"Fetching decision version: {versionId}")
        return self._get_and_parse(Decision, DECISIONS, "v", versionId)

    def get_a_decisions_version_log(self, decisions_uid: str) -> DecisionVersions:
        """Returns details of a specific version of a decision."""
        logger.info(f"Fetching version log for decision: {decisions_uid}")
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
        logger.info(f"Fetching organizations (status={status}, category={category})")

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
        logger.info(f"Fetching organization details: {organization_id}")
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
        logger.info(f"Fetching units for organization: {organization_id}")
        return self._get_and_parse(UnitsResponse, ORGANIZATIONS, organization_id, UNITS)

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
        logger.info(f"Fetching signers for organization: {organization_id}")
        return self._get_and_parse(
            SignersResponse, ORGANIZATIONS, organization_id, SIGNERS
        )

    # TODO: Add a test for this method
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
        logger.info(f"Fetching positions for organization: {organization_id}")
        return self._get_and_parse(
            PositionsResponse, ORGANIZATIONS, organization_id, POSITIONS
        )

    def get_all_types(
        self,
    ) -> TypeSummaries:
        """
        Returns all existing types.

        Parameters
        ----------
        organization_id : str
            The unique identifier of the organization.
        """
        logger.info("Fetching all decision types")
        return self._get_and_parse(TypeSummaries, TYPES)

    def get_a_types_summary(
        self,
        types_uid: str,
    ) -> TypeSummary:
        """
        Returns a summary of a specific type.

        Parameters
        ----------
        types_uid : str
            The unique identifier of the type.
        """
        logger.info(f"Fetching summary for type: {types_uid}")
        return self._get_and_parse(TypeSummary, TYPES, types_uid)

    def get_a_types_details(
        self,
        types_uid: str,
    ) -> TypeDetails:
        """
        Returns details of a type.

        Parameters
        ----------
        types_uid : str
            The unique identifier of the types_uid.
        """
        logger.info(f"Fetching details for type: {types_uid}")
        return self._get_and_parse(TypeDetails, TYPES, types_uid, "details")

    def search_decisions(
        self,
        ada: Optional[str] = None,
        subject: Optional[str] = None,
        protocol: Optional[str] = None,
        term: Optional[str] = None,
        org: Optional[Union[str, List[str]]] = None,
        unit: Optional[Union[str, List[str]]] = None,
        signer: Optional[Union[str, List[str]]] = None,
        type: Optional[Union[str, List[str]]] = None,
        tag: Optional[Union[str, List[str]]] = None,
        from_date: Optional[Union[str, datetime.date]] = None,
        to_date: Optional[Union[str, datetime.date]] = None,
        from_issue_date: Optional[Union[str, datetime.date]] = None,
        to_issue_date: Optional[Union[str, datetime.date]] = None,
        status: Optional[DecisionStatus] = DecisionStatus.PUBLISHED,
        page: int = 0,
        size: Optional[int] = None,
        sort: SortOrder = SortOrder.RECENT,
    ) -> SearchResponse:
        """
        Search for decisions with simple parameters.

        Args:
            ada: Αριθμός Διαδικτυακής Ανάρτησης
            subject: Θέμα πράξης
            protocol: Αριθμός Πρωτοκόλλου
            term: Γενικός όρος αναζήτησης
            org: Κωδικός ή latin name φορέα (can be multiple values separated by ';')
            unit: Κωδικός οργανωτικής μονάδας (can be multiple values separated by ';')
            signer: Κωδικός υπογράφοντα (can be multiple values separated by ';')
            type: Κωδικός τύπου πράξεων (can be multiple values separated by ';')
            tag: Κωδικός θεματικών ενοτήτων (can be multiple values separated by ';')
            from_date: Ημερομηνία τελευταίας τροποποίησης - Από (format: YYYY-MM-DD)
            to_date: Ημερομηνία τελευταίας τροποποίησης - Έως (format: YYYY-MM-DD)
            from_issue_date: Ημερομηνία έκδοσης - Από (format: YYYY-MM-DD)
            to_issue_date: Ημερομηνία έκδοσης - Έως (format: YYYY-MM-DD)
            status: Κατάσταση πράξης (published, revoked, pending_revocation, all)
            page: Αριθμός σελίδας αποτελεσμάτων (0-based)
            size: Μέγεθος σελίδας αποτελεσμάτων
            sort: Είδος ταξινόμησης (recent, relative)

        Returns:
            SearchResponse: The search results
        """
        logger.info("Searching for decisions with simple parameters")
        logger.debug(
            f"Search parameters: ada={ada}, subject={subject}, term={term}, page={page}, size={size}"
        )

        params = {}

        # Add parameters only if they're provided
        if ada:
            params["ada"] = ada
        if subject:
            params["subject"] = subject
        if protocol:
            params["protocol"] = protocol
        if term:
            params["term"] = term

        # Handle list parameters that can have multiple values
        for param_name, param_value in [
            ("org", org),
            ("unit", unit),
            ("signer", signer),
            ("type", type),
            ("tag", tag),
        ]:
            if param_value:
                if isinstance(param_value, list):
                    # Join multiple values with Greek question mark
                    params[param_name] = ";".join(param_value)
                else:
                    params[param_name] = param_value

        # Handle date parameters
        for param_name, param_value in [
            ("from_date", from_date),
            ("to_date", to_date),
            ("from_issue_date", from_issue_date),
            ("to_issue_date", to_issue_date),
        ]:
            if param_value:
                if isinstance(param_value, datetime.date):
                    # Convert date object to string format
                    params[param_name] = param_value.strftime(WANTED_DATE_FORMAT)
                else:
                    params[param_name] = param_value

        # Add remaining parameters
        if status:
            params["status"] = (
                status.value if isinstance(status, DecisionStatus) else status
            )

        params["page"] = page
        if size:
            params["size"] = size

        params["sort"] = sort.value if isinstance(sort, SortOrder) else sort

        logger.debug(f"Final search parameters: {params}")
        response = self._get_and_parse(SearchResponse, SEARCH, params=params)
        logger.info(f"Search returned {response.info.total} results")
        return response

    def search_advanced(
        self,
        q: str,
        page: int = 0,
        size: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search for decisions with advanced query syntax.

        Args:
            q: Advanced search query using the Diavgeia query syntax
            page: Page number (0-based)
            size: Page size
            sort: Sort order (e.g., "issueDate:desc")

        Returns:
            SearchResponse: The search results
        """
        logger.info("Performing advanced search")
        logger.debug(f"Advanced query: {q}")

        params = {"q": q, "page": page}

        if size:
            params["size"] = size

        if sort:
            params["sort"] = sort

        response = self._get_and_parse(
            SearchResponse, SEARCH, "advanced", params=params
        )
        logger.info(f"Advanced search returned {response.info.total} results")
        return response
