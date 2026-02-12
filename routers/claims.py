from fastapi import APIRouter
from database import get_db

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.post("/submit")
def submit_claim(data: dict):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO claims
        (item_id, claimer_id, claim_description,
         claim_location, claim_time)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            data["item_id"],
            data["claimer_id"],
            data["claim_description"],
            data["claim_location"],
            data["claim_time"]
        )
    )
    db.commit()
    return {"message": "Claim submitted"}
