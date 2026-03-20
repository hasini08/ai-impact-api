from sqlalchemy import Column, Float, Integer, String

from database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    occupation_code = Column(String, nullable=True, index=True)
    created_at = Column(String, nullable=False)

    verification_status = Column(String, nullable=False, default="unverified")
    impact_score = Column(Float, nullable=False, default=0.5)
    source_type = Column(String, nullable=False, default="article")


class AIExposureScore(Base):
    __tablename__ = "ai_exposure_scores"

    id = Column(Integer, primary_key=True, index=True)
    occupation_code = Column(String, unique=True, index=True, nullable=False)
    occupation_title = Column(String, nullable=False)
    exposure_score = Column(Float, nullable=False)