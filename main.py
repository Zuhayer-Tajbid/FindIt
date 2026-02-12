from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, items, claims, admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)   # ← THIS LINE IS REQUIRED
app.include_router(claims.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"status": "backend working"}
