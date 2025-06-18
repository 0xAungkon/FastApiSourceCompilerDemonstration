from fastapi import FastAPI
from app.routers import posts as posts_router

app = FastAPI()

app.include_router(posts_router.router, prefix="/api", tags=["posts"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Blog API"}
