from app.db.session import db
from app.models.user import UserModel, UserRole
from app.core.security import get_password_hash, verify_password
from bson import ObjectId

async def create_user(email: str, password: str, role: UserRole, org_id: str):
    hashed = get_password_hash(password)
    user = UserModel(
        email=email,
        hashed_password=hashed,
        role=role,
        org_id=org_id
    )
    result = await db.users.insert_one(user.dict(by_alias=True))
    user.id = result.inserted_id
    return user


async def authenticate_user(email: str, password: str, org_id: str):
    user = await db.users.find_one({
        "email": email,
        "org_id": ObjectId(org_id)
    })
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


