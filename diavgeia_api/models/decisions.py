from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Normalized models for typical usage
class Attachment(BaseModel):
    id: str
    description: Optional[str] = None
    filename: str
    mime_type: str = Field(..., alias="mimeType")
    checksum: str  # SHA-1 hash of the attachment file


# Exact JSON structure models
class DecisionAPI(BaseModel):
    protocolNumber: Optional[str] = None
    subject: str
    issueDate: int  # Unix epoch (ms) of issue date
    organizationId: str
    signerIds: List[str]
    unitIds: List[str]
    decisionTypeId: str
    thematicCategoryIds: List[str]
    privateData: bool
    submissionTimestamp: int  # Unix epoch (ms) of last submission time
    publishTimestamp: Optional[int] = None
    status: str  # e.g. "PUBLISHED", "REVOKED", "PENDING_REVOCATION"&#8203;:contentReference[oaicite:8]{index=8}
    ada: Optional[str] = None  # ADA (if published)
    versionId: str
    correctedVersionId: Optional[str] = None
    documentUrl: Optional[str] = None  # URL for main document PDF
    documentChecksum: Optional[str] = (
        None  # SHA-1 of main document&#8203;:contentReference[oaicite:9]{index=9}
    )
    url: Optional[str] = None  # API URL of this decision
    # Attachments: list of attached documents (each with id, description, filename, etc.)&#8203;:contentReference[oaicite:10]{index=10}
    attachments: List[Attachment] = []  # (Exact structure as dict to mirror raw JSON)
    warnings: Optional[str] = None
    extraFieldValues: Optional[dict] = (
        None  # Additional fields (vary by decision type)&#8203;:contentReference[oaicite:11]{index=11}
    )


class DecisionListAPI(BaseModel):
    decisions: List[DecisionAPI]
    info: dict  # Contains pagination info: page, size, total, order, etc.&#8203;:contentReference[oaicite:12]{index=12}&#8203;:contentReference[oaicite:13]{index=13}


class Decision(BaseModel):
    protocol_number: Optional[str] = Field(None, alias="protocolNumber")
    subject: str
    issue_date: datetime = Field(..., alias="issueDate")
    organization_id: str = Field(..., alias="organizationId")
    signer_ids: List[str] = Field(..., alias="signerIds")
    unit_ids: List[str] = Field(..., alias="unitIds")
    decision_type_id: str = Field(..., alias="decisionTypeId")
    thematic_category_ids: List[str] = Field(..., alias="thematicCategoryIds")
    private_data: bool = Field(..., alias="privateData")
    submission_timestamp: datetime = Field(..., alias="submissionTimestamp")
    publish_timestamp: Optional[datetime] = Field(None, alias="publishTimestamp")
    status: str
    ada: Optional[str] = None
    version_id: str = Field(..., alias="versionId")
    corrected_version_id: Optional[str] = Field(None, alias="correctedVersionId")
    document_url: Optional[str] = Field(None, alias="documentUrl")
    document_checksum: Optional[str] = Field(None, alias="documentChecksum")
    url: Optional[str] = None
    attachments: List[Attachment] = []
    warnings: Optional[str] = None
    extra_field_values: Optional[dict] = Field(None, alias="extraFieldValues")


class PageInfo(BaseModel):
    page: int
    size: int
    total: int
    order: str
    query: Optional[str] = None
    actual_size: Optional[int] = Field(
        None, alias="actualSize"
    )  # actual results returned


class DecisionList(BaseModel):
    decisions: List[Decision]
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
