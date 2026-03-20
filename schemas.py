from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


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


class SourceTypeEnum(str, Enum):
    article = "article"
    report = "report"
    blog = "blog"
    research = "research"
    news = "news"


class ClaimBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    category: CategoryEnum
    description: str = Field(..., min_length=10, max_length=1000)
    source_url: HttpUrl
    occupation_code: Optional[str] = Field(None, min_length=2, max_length=10)
    verification_status: VerificationStatusEnum = VerificationStatusEnum.unverified
    impact_score: float = Field(0.5, ge=0.0, le=1.0)
    source_type: SourceTypeEnum = SourceTypeEnum.article


class ClaimCreate(ClaimBase):
    pass


class ClaimUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    category: Optional[CategoryEnum] = None
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    source_url: Optional[HttpUrl] = None
    occupation_code: Optional[str] = Field(None, min_length=2, max_length=10)
    verification_status: Optional[VerificationStatusEnum] = None
    impact_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    source_type: Optional[SourceTypeEnum] = None


class ClaimOut(ClaimBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class AIExposureOut(BaseModel):
    occupation_code: str
    occupation_title: str
    exposure_score: float

    class Config:
        from_attributes = True


class CategoryCountOut(BaseModel):
    category: str
    count: int


class SummaryOut(BaseModel):
    total_claims: int
    average_impact_score: float
    total_occupations: int