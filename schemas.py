from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


# ---- ENUMS ----
class CategoryEnum(str, Enum):
    jobs = "jobs"
    creativity = "creativity"
    environment = "environment"
    education = "education"
    ethics = "ethics"


class VerificationStatusEnum(str, Enum):
    unverified = "unverified"
    reviewed = "reviewed"
    supported = "supported"
    disputed = "disputed"


# ---- BASE CLAIM ----
class ClaimBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    category: CategoryEnum
    description: str = Field(..., min_length=10, max_length=1000)
    source_url: HttpUrl
    occupation_code: Optional[str] = Field(None, min_length=2, max_length=10)


# ---- CREATE ----
class ClaimCreate(ClaimBase):
    pass


# ---- UPDATE ----
class ClaimUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    category: Optional[CategoryEnum]
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    source_url: Optional[HttpUrl]
    occupation_code: Optional[str] = Field(None, min_length=2, max_length=10)


# ---- RESPONSE ----
class ClaimOut(ClaimBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


# ---- ANALYTICS ----
class AIExposureOut(BaseModel):
    occupation_code: str
    occupation_title: str
    exposure_score: float

    class Config:
        from_attributes = True