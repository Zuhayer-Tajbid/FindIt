from fastapi import APIRouter
from database import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/claims")
def get_pending_claims():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT c.id AS claim_id, c.status,
               u.name, u.roll,
               i.title, i.detailed_description,
               c.claim_description, c.claim_location
        FROM claims c
        JOIN users u ON c.claimer_id = u.id
        JOIN items i ON c.item_id = i.id
        WHERE c.status='pending'
        ORDER BY c.created_at DESC
        """
    )
    return cursor.fetchall()

@router.post("/claim/{claim_id}/approve")
def approve_claim(claim_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE claims SET status='approved' WHERE id=%s",
        (claim_id,)
    )

    cursor.execute(
        """
        UPDATE items
        SET status='resolved'
        WHERE id=(SELECT item_id FROM claims WHERE id=%s)
        """,
        (claim_id,)
    )

    db.commit()
    return {"message": "Claim approved"}

@router.post("/claim/{claim_id}/reject")
def reject_claim(claim_id: int):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE claims SET status='rejected' WHERE id=%s",
        (claim_id,)
    )
    db.commit()
    return {"message": "Claim rejected"}
