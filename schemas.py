from pydantic import BaseModel
from typing import Optional

class ClaimCreate(BaseModel):
    title: str
    category: str
    description: str
    source_url: Optional[str] = None
    occupation_code: Optional[str] = None

class ClaimUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    source_url: Optional[str] = None
    occupation_code: Optional[str] = None

class ClaimOut(BaseModel):
    id: int
    title: str
    category: str
    description: str
    source_url: Optional[str]
    occupation_code: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

class AIExposureOut(BaseModel):
    occupation_code: str
    occupation_title: str
    exposure_score: float

    class Config:
        from_attributes = True