"""Analysis request and response schemas."""

from typing import Literal

from pydantic import BaseModel

SectionStatus = Literal["present", "weak", "missing"]


class SectionAnalysisItem(BaseModel):
    """Section status and user-facing Turkish message."""

    section: str
    status: SectionStatus
    message: str
