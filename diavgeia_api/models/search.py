from typing import List, Optional, Any, Dict, Union
from enum import Enum
from pydantic import BaseModel, Field
import datetime
from .decisions import Decision


class SortOrder(str, Enum):
    """Είδος ταξινόμησης."""

    RECENT = (
        "recent"  # Φθίνουσα ταξινόμηση ως προς την ημερομηνία τελευταίας τροποποίησης
    )
    RELATIVE = (
        "relative"  # Φθίνουσα ταξινόμηση ως προς τη σχετικότητα των αποτελεσμάτων
    )


class SearchInfo(BaseModel):
    """Information about the search results."""

    query: str
    page: int
    size: int
    actualSize: int
    total: int
    order: str


class SearchResponse(BaseModel):
    """Response model for search endpoints."""

    decisions: List[Decision]
    info: SearchInfo
