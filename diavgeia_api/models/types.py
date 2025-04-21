import sys
from typing import List, Optional, Any
from typing import Self
from typing_extensions import Self
from pydantic import BaseModel, Field


class TypeSummary(BaseModel):
    """
    Represents the summary information for an act type.
    Corresponds to the output of GET /types/:uid
    """

    uid: str = Field(..., description="Κωδικός τύπου πράξεων")
    label: str = Field(..., description="Ετικέτα τύπου πράξεων")
    allowedInDecisions: bool = Field(
        ...,
        description="Αν ο τύπος επιτρέπεται σε αποφάσεις",
    )


class TypeSummaries(BaseModel):
    decisionTypes: List[TypeSummary]


class ExtraField(BaseModel):
    """
    Represents the structure of an extra field within a detailed act type.
    """

    uid: str = Field(..., description="Μοναδικός κωδικός πεδίου")
    label: Optional[str] = Field(None, description="Ετικέτα πεδίου")

    # Changed to Optional because it can be None too, like in here:
    # {
    #         "uid": "documentType",
    #         "label": null,
    #         "help": null,
    #         "type": "string",
    #         "validation": null,
    #         "required": false,
    #         "multiple": false,
    #         "maxLength": 0,
    #         "dictionary": null,
    #         "searchTerm": "documentType",
    #         "relAdaDecisionTypes": null,
    #         "relAdaConstrainedInOrganization": null,
    #         "fixedValueList": null,
    #         "nestedFields": []
    #     }
    type: str = Field(..., description="Τύπος δεδομένων πεδίου (π.χ., string, object)")
    validation: Optional[str] = Field(
        None, description="Κανόνας επικύρωσης (π.χ., ada)"
    )
    required: bool = Field(..., description="Αν το πεδίο είναι υποχρεωτικό")
    multiple: bool = Field(
        ..., description="Αν το πεδίο μπορεί να έχει πολλαπλές τιμές"
    )
    maxLength: int = Field(..., description="Μέγιστο μήκος (0 αν δεν υπάρχει όριο)")
    dictionary: Optional[str] = Field(None, description="Κωδικός λεξικού τιμών")
    searchTerm: Optional[str] = Field(
        None,
        description="Όρος αναζήτησης που αντιστοιχεί στο πεδίο",
    )
    relAdaDecisionTypes: Optional[Any] = Field(
        None,
        description="Συσχετιζόμενοι τύποι πράξεων ΑΔΑ",
    )
    relAdaConstrainedInOrganization: Optional[bool] = Field(
        None,
        description="Περιορισμός βάσει οργανισμού για σχετιζόμενες πράξεις ΑΔΑ",
    )
    nestedFields: List[Self] = Field(
        default_factory=list,
        description="Λίστα ενσωματωμένων πεδίων (για type='object')",
    )


class TypeDetails(TypeSummary):
    """
    Represents the detailed information for an act type, including extra fields.
    Corresponds to the output of GET /types/:uid/details
    """

    parent: Optional[str] = Field(
        None, description="Μοναδικός κωδικός γονικού πεδίου (αν υπάρχει)"
    )
    extraFields: List[ExtraField] = Field(
        default_factory=list,
        description="Λίστα ειδικών πεδίων που ορίζονται στον τύπο πράξης",
    )
