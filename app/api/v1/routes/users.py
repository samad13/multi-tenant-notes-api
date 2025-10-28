from fastapi import APIRouter, Path, Body, HTTPException
from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin
from app.services.user_service import create_user, authenticate_user
from app.db.session import db
from bson import ObjectId
from app.core.security import create_access_token

router = APIRouter()

@router.post("/", response_model=dict)
async def create_user_in_org(
    org_id: str = Path(...),
    user: UserCreate = Body(...)
):
    if not await db.organizations.find_one({"_id": ObjectId(org_id)}):
        raise HTTPException(status_code=404, detail="Organization not found")
    created = await create_user(
        email=user.email,
        password=user.password,
        role=user.role,
        org_id=org_id
    )
    token = create_access_token({"sub": str(created.id), "org": org_id})
    return {
        "user_id": str(created.id),
        "email": created.email,
        "role": created.role,
        "access_token": token
    }



@router.post("/login", response_model=dict)
async def login_user(
    org_id: str = Path(...),
   login_data: UserLogin = Body(...)
):
    if not await db.organizations.find_one({"_id": ObjectId(org_id)}):
        raise HTTPException(status_code=404, detail="Organization not found")
    
    user = await authenticate_user(login_data.email, login_data.password, org_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({
        "sub": str(user["_id"]),
        "org": org_id
    })
    return {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],
        "access_token": token
    }