from typing import List, Optional
from pydantic import BaseModel, HttpUrl, field_validator
from enum import Enum
import datetime

# --- Enums based on documentation ---


class OrganizationStatus(str, Enum):
    """Κατάσταση φορέα."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class UnitDescendants(str, Enum):
    """Επίπεδο επιστροφής μονάδων."""

    CHILDREN = "children"
    ALL = "all"


class UnitStatus(str, Enum):
    """Κατάσταση μονάδων."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ALL = "all"


# --- Models for /organizations endpoint ---


class Organization(BaseModel):
    """Represents a single organization. Uses API field names directly."""

    uid: str
    latinName: str
    abbreviation: Optional[str] = None
    label: str
    status: OrganizationStatus
    category: str
    vatNumber: Optional[str] = None
    fekNumber: Optional[str] = None
    fekIssue: Optional[str] = None
    fekYear: Optional[str] = None
    organizationDomains: Optional[List[str]] = None
    # website: Optional[HttpUrl] = None
    # Receiving API is not actually validating this field as a URL, so it can be any string.
    # I even found den gnvr;izv:
    #     "odeManagerEmail": "tkerodopis@yeka.gr",
    # "website": "http://den gnvr;izv",
    # "supervisorId": "100081533",
    # "supervisorLabel": "ΥΠΟΥΡΓΕΙΟ ΕΡΓΑΣΙΑΣ ΚΑΙ ΚΟΙΝΩΝΙΚΗΣ ΑΣΦΑΛΙΣΗΣ",
    # "organizationDomains": []
    #  Input should be a valid URL, invalid international domain name [type=url_parsing, input_value='http://den gnvr;izv', input_type=str]
    website: Optional[str] = None

    supervisorOrgUid: Optional[str] = None
    supervisorOrgName: Optional[str] = None

    class ConfigDict:
        use_enum_values = True

    @field_validator("website", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """Convert empty string for website to None before validation."""
        if isinstance(v, str) and v == "":
            return None
        return v


class OrganizationsResponse(BaseModel):
    """Response model for listing organizations."""

    organizations: List[Organization]


# --- Models for /organizations/:org/units endpoint ---


class Unit(BaseModel):
    """Represents a single organizational unit. Uses API field names directly."""

    uid: str
    label: str
    active: bool
    activeFrom: Optional[datetime.datetime] = None
    activeUntil: Optional[datetime.datetime] = None
    category: str
    unitDomains: Optional[List[str]] = None
    parentId: str


class UnitsResponse(BaseModel):
    """Response model for listing organizational units."""

    units: List[Unit]


# --- Models for /organizations/:org/signers endpoint ---


class SignerUnit(BaseModel):
    """Represents a unit associated with a signer."""

    uid: str
    positionId: str
    positionLabel: str


class Signer(BaseModel):
    """Represents a single signer. Uses API field names directly."""

    uid: str
    firstName: str
    lastName: str
    active: bool
    activeFrom: Optional[datetime.datetime] = None
    activeUntil: Optional[datetime.datetime] = None
    organizationId: str
    hasOrganizationSignRights: bool
    units: List[SignerUnit]

    @field_validator("activeFrom", "activeUntil", mode="before")
    @classmethod
    def timestamp_ms_to_datetime(cls, v):
        """Convert timestamp in milliseconds to datetime object."""
        if v is not None:
            # Convert milliseconds to seconds
            return datetime.datetime.fromtimestamp(v / 1000, tz=datetime.timezone.utc)
        return None


class SignersResponse(BaseModel):
    """Response model for listing signers of an org."""

    # The list should contain Signer objects, not Unit objects.
    signers: List[Signer]
