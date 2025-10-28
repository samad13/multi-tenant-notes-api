from pydantic import BaseModel, EmailStr
from typing import Literal

UserRole = Literal["reader", "writer", "admin"]

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole


