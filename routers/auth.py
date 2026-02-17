from fastapi import APIRouter, HTTPException
from database import get_db
import hashlib

router = APIRouter(prefix="/auth", tags=["Auth"])

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/signup")
def signup(data: dict):
    db = get_db()
    cursor = db.cursor()

    password_hash = hash_password(data["password"])

    try:
        cursor.execute(
            """
            INSERT INTO users (name, roll, email, password_hash)
            VALUES (%s, %s, %s, %s)
            """,
            (data["name"], data["roll"], data["email"], password_hash)
        )
        db.commit()
        return {"message": "Account created"}
    except:
        raise HTTPException(status_code=400, detail="Email already exists")

@router.post("/login")
def login(data: dict):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    password_hash = hash_password(data["password"])

    cursor.execute(
        """
        SELECT id, name, roll, email, role
        FROM users
        WHERE email=%s AND password_hash=%s
        """,
        (data["email"], password_hash)
    )

    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cursor.close()
    db.close()

    return user


@router.get("/users")
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, roll, email, role
        FROM users
    """)

    users = cursor.fetchall()

    cursor.close()
    db.close()

    return users

@router.get("/auth/test-db")
def test_db():
    db = get_db()
    return {"db": "connected"}
