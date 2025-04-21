from pydantic import BaseModel, Field
from typing import Any, List, Optional
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


class AmountWithKAE(BaseModel):
    """Amount with KAE (Κωδικός Αριθμού Εξόδου)."""

    kae: str
    amountWithVAT: float


class Amount(BaseModel):
    """Amount with currency."""

    amount: float
    currency: str


class ExtraFieldValues(BaseModel):
    """Extra fields that may be present in a decision."""

    financialYear: Optional[int] = None
    budgettype: Optional[str] = None
    entryNumber: str
    recalledExpenseDecision: Optional[bool] = None
    amountWithVAT: Optional[Amount] = None
    amountWithKae: Optional[List[AmountWithKAE]] = None
    partialead: Optional[bool] = None
    relatedDecisions: List[Any] = Field(default_factory=list)
    documentType: Optional[str] = None


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
