from fastapi import APIRouter
from database import get_db
from schemas.claim import ClaimCreate

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.post("/submit")
def submit_claim(data: ClaimCreate):
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
            data.item_id,
            data.claimer_id,
            data.claim_description,
            data.claim_location,
            data.claim_time,
        )
    )
    db.commit()

    return {"success": True}

@router.get("/")
def get_claims(user_id: int | None = None):
    """
    If user_id is provided → return only that user's claims
    If not → return all claims
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if user_id:
        cursor.execute(
            """
            SELECT
              c.id,
              c.item_id,
              c.claimer_id,
              c.claim_description,
              c.claim_location,
              c.claim_time,
              c.status AS claim_status,
              i.title AS item_title,
              i.category
            FROM claims c
            JOIN items i ON c.item_id = i.id
            WHERE c.claimer_id = %s
            ORDER BY c.claim_time DESC
            """,
            (user_id,)
        )
    else:
        cursor.execute(
            """
            SELECT
              c.id,
              c.item_id,
              c.claimer_id,
              c.claim_description,
              c.claim_location,
              c.claim_time,
              c.status AS claim_status,
              i.title AS item_title,
              i.category
            FROM claims c
            JOIN items i ON c.item_id = i.id
            ORDER BY c.claim_time DESC
            """
        )

    claims = cursor.fetchall()
    return claims

@router.delete("/{claim_id}")
def delete_claim(claim_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM claims WHERE id = %s",
        (claim_id,)
    )

    db.commit()
    cursor.close()
    db.close()

    return {"success": True}


@router.put("/{claim_id}")
def update_claim(claim_id: int, data: ClaimCreate):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE claims
        SET
            claim_description = %s,
            claim_location = %s,
            claim_time = %s
        WHERE id = %s
        """,
        (
            data.claim_description,
            data.claim_location,
            data.claim_time,
            claim_id
        )
    )

    db.commit()
    cursor.close()
    db.close()

    return {"success": True}