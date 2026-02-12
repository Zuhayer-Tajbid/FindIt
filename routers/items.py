from fastapi import APIRouter
from database import get_db

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/report")
def report_item(data: dict):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO items
        (title, short_description, detailed_description,
         category, status, location, event_time, reporter_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            data["title"],
            data["short_description"],
            data["detailed_description"],
            data["category"],
            data["status"],
            data["location"],
            data["event_time"],
            data["reporter_id"]
        )
    )
    db.commit()
    return {"message": "Item reported"}

@router.get("/")
def list_items():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, short_description, category,
               status, location, event_time
        FROM items
        ORDER BY created_at DESC
        """
    )
    return cursor.fetchall()
