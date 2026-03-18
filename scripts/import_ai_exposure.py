import sys
import os
import csv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal
from models import AIExposureScore

db = SessionLocal()

with open("scripts/ai_exposure_sample.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        item = AIExposureScore(
            occupation_code=row["occupation_code"],
            occupation_title=row["occupation_title"],
            exposure_score=float(row["exposure_score"])
        )
        db.add(item)

db.commit()
db.close()

print("Import complete.")