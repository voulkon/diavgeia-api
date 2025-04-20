from typing import List, Optional, Union
from pydantic import BaseModel, HttpUrl
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
    abbreviation: str
    label: str
    status: OrganizationStatus
    category: str
    vatNumber: Optional[str] = None
    fekNumber: Optional[str] = None
    fekIssue: Optional[str] = None
    fekYear: Optional[str] = None
    website: Optional[HttpUrl] = None
    organizationDomains: List[str]
    supervisorOrgUid: Optional[str] = None
    supervisorOrgName: Optional[str] = None

    class ConfigDict:
        use_enum_values = True


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
    unitDomains: List[str]
    parentId: str


class UnitsResponse(BaseModel):
    """Response model for listing organizational units."""

    units: List[Unit]
