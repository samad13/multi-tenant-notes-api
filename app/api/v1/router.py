from fastapi import APIRouter
from app.api.v1.routes import organizations, users, notes

api_router = APIRouter()

api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(users.router, prefix="/organizations/{org_id}/users", tags=["users"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])