from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Attachment(BaseModel):
    id: str
    description: Optional[str] = None
    filename: str
    mimeType: str
    checksum: str


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
    status: str
    ada: Optional[str] = None
    versionId: str
    correctedVersionId: Optional[str] = None
    documentUrl: Optional[str] = None
    documentChecksum: Optional[str] = None
    url: Optional[str] = None
    attachments: List[Attachment] = []
    warnings: Optional[str] = None
    extraFieldValues: Optional[dict] = None


class PageInfo(BaseModel):
    page: int
    size: int
    total: int
    order: str
    query: Optional[str]
    actualSize: Optional[int]


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
