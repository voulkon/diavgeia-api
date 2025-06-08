from pydantic import BaseModel, ConfigDict
from typing import Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class DecisionStatus(str, Enum):
    """Κατάσταση πράξης."""

    PUBLISHED = "PUBLISHED"
    REVOKED = "REVOKED"  # Ανακληθείσα
    PENDING_REVOCATION = "PENDING_REVOCATION"  # Εν αναμονή ανάκλησης
    ALL = "ALL"


class Attachment(BaseModel):
    id: str
    description: Optional[str] = None
    filename: str
    mimeType: str
    checksum: str

# FLEXIBLE TYPE for fields that might vary
FlexibleValue = Union[str, int, float, bool, dict, list, None]

class AmountWithKAE(BaseModel):
    """Amount with KAE - flexible because Diavgeia is chaos."""

    # Core fields - prefer expected types but accept anything
    kae: Union[str, FlexibleValue] = None  # Usually string, but might be complex
    amountWithVAT: Union[float, FlexibleValue] = None  # Usually float, but might be dict
    
    # Capture everything else
    model_config = ConfigDict(extra='allow')


class Amount(BaseModel):
    """Amount - flexible for unexpected structures."""

    amount: Union[float, FlexibleValue] = None  # Could be {"value": 100, "formatted": "100.00 EUR"}
    currency: Union[str, FlexibleValue] = None  # Could be {"code": "EUR", "symbol": "€"}
    
    model_config = ConfigDict(extra='allow')


class ExtraFieldValues(BaseModel):
    """Extra fields - maximum flexibility with intelligent defaults."""

    # Known fields with flexible typing
    financialYear: Union[int, FlexibleValue] = None  # Usually int, but could be {"year": 2025, "quarter": 1}
    budgettype: Union[str, FlexibleValue] = None     # Usually string, but could be {"type": "regular", "subtype": "main"}
    entryNumber: Union[str, FlexibleValue] = None    # CONCERN: could be {"primary": "1802", "secondary": "1497"}
    recalledExpenseDecision: Union[bool, FlexibleValue] = None
    amountWithVAT: Union[Amount, FlexibleValue] = None
    amountWithKae: Union[List[AmountWithKAE], FlexibleValue] = None  # Could be dict with metadata
    partialead: Union[bool, FlexibleValue] = None
    relatedDecisions: Union[List[Any], FlexibleValue] = None
    documentType: Union[str, FlexibleValue] = None
    awardAmount: Union[Amount, FlexibleValue] = None
    
    model_config = ConfigDict(extra='allow')


class Decision(BaseModel):
    protocolNumber: Optional[str] = None
    subject: str
    issueDate: datetime
    organizationId: str
    signerIds: List[str]
    unitIds: List[str]
    decisionTypeId: str
    thematicCategoryIds: List[str]
    privateData: bool
    submissionTimestamp: datetime
    publishTimestamp: Optional[datetime] = None
    status: DecisionStatus
    ada: Optional[str] = None
    versionId: str
    correctedVersionId: Optional[str] = None
    documentUrl: Optional[str] = None
    documentChecksum: Optional[str] = None
    url: Optional[str] = None
    attachments: List[Attachment] = []
    warnings: Optional[str] = None
    extraFieldValues: Optional[ExtraFieldValues] = None


class PageInfo(BaseModel):
    page: int
    size: int
    total: int
    order: str
    query: Optional[str]
    actualSize: Optional[int]


class DecisionList(BaseModel):
    decisions: List[Decision]
    # TODO: Implement pagination mechanism
    info: PageInfo


class Version(BaseModel):
    versionId: str
    creator: str
    versionTimestamp: datetime
    description: Optional[str] = None
    status: str
    correctedVersionId: Optional[str]


class DecisionVersions(BaseModel):
    ada: str
    organizationId: str
    versions: List[Version]
