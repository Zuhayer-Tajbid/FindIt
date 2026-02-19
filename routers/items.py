from fastapi import APIRouter
from database import get_db
from schemas.items import ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/report")
def report_item(data: ItemCreate):
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
            data.title,
            data.short_description,
            data.detailed_description,
            data.category,
            data.status,
            data.location,
            data.event_time,
            data.reporter_id
        )
    )

    db.commit()
    return {"message": "Item reported successfully"}


@router.get("/")
def list_items():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
          i.id,
          i.title,
          i.short_description,
          i.category,
          i.status,
          i.location,
          i.event_time,

          u.id   AS user_id,
          u.name AS user_name,
          u.roll AS user_roll

        FROM items i
        JOIN users u ON i.reporter_id = u.id
        ORDER BY i.created_at DESC
        """
    )

    items = cursor.fetchall()
    cursor.close()
    db.close()

    return items

@router.delete("/{item_id}")
def delete_item(item_id: int):
    db = get_db()
    cursor = db.cursor()

    # Optional: delete related claims first (if foreign key not cascading)
    cursor.execute(
        "DELETE FROM claims WHERE item_id = %s",
        (item_id,)
    )

    cursor.execute(
        "DELETE FROM items WHERE id = %s",
        (item_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return {"success": True}
