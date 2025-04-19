from typing import List, Optional
from pydantic import BaseModel


class DictionaryItem(BaseModel):
    uid: str
    label: str
    parent: Optional[str] = None


class DictionaryValuesResponse(BaseModel):
    name: str
    items: List[DictionaryItem]


class DictionaryListItem(BaseModel):
    uid: str
    label: str


class DictionariesListResponse(BaseModel):
    dictionaries: List[DictionaryListItem]
