from sqlalchemy import Column, Integer, String, Text, Float
from database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    source_url = Column(String, nullable=True)
    occupation_code = Column(String, nullable=True)
    created_at = Column(String, nullable=False)

class AIExposureScore(Base):
    __tablename__ = "ai_exposure_scores"

    id = Column(Integer, primary_key=True, index=True)
    occupation_code = Column(String, nullable=False, index=True)
    occupation_title = Column(String, nullable=False)
    exposure_score = Column(Float, nullable=False)