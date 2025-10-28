from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from app.models.common import PyObjectId

UserRole = Literal["reader", "writer", "admin"]

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    role: UserRole
    org_id: PyObjectId

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
