from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import AIExposureScore, Claim
from schemas import AIExposureOut, ClaimCreate, ClaimOut, ClaimUpdate
from security import require_api_key


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Impact Claims API",
    description="A data-driven FastAPI project exploring AI's impact on jobs, creativity, and the environment.",
    version="1.1.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "AI Impact Claims API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/claims", response_model=ClaimOut, status_code=status.HTTP_201_CREATED)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    db_claim = Claim(
        title=claim.title,
        category=claim.category,
        description=claim.description,
        source_url=claim.source_url,
        occupation_code=claim.occupation_code,
        created_at=datetime.utcnow().isoformat(),
    )

    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)

    return db_claim


@app.get("/claims", response_model=list[ClaimOut])
def get_claims(db: Session = Depends(get_db)):
    return db.query(Claim).all()


@app.get("/claims/{claim_id}", response_model=ClaimOut)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    return claim


@app.patch("/claims/{claim_id}", response_model=ClaimOut)
def update_claim(
    claim_id: int,
    update: ClaimUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    if update.title is not None:
        claim.title = update.title

    if update.category is not None:
        claim.category = update.category

    if update.description is not None:
        claim.description = update.description

    if update.source_url is not None:
        claim.source_url = update.source_url

    if update.occupation_code is not None:
        claim.occupation_code = update.occupation_code

    db.commit()
    db.refresh(claim)

    return claim


@app.delete("/claims/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    db.delete(claim)
    db.commit()
    return None


@app.get("/analytics/high-exposure", response_model=list[AIExposureOut])
def high_exposure(
    min_score: float = Query(0.7, ge=0, le=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    results = (
        db.query(AIExposureScore)
        .filter(AIExposureScore.exposure_score >= min_score)
        .order_by(AIExposureScore.exposure_score.desc())
        .limit(limit)
        .all()
    )

    return results