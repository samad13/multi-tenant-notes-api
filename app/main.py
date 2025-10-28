from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Multi-Tenant Notes API")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Multi-Tenant Notes API"}