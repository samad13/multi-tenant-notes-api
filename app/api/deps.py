from fastapi import Depends, HTTPException
from typing import Literal
from app.core.auth import get_current_user

def require_role(required_role: Literal["reader", "writer", "admin"]):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        role_hierarchy = {"reader": 0, "writer": 1, "admin": 2}
        user_role = current_user["role"]

        if role_hierarchy[user_role] < role_hierarchy[required_role]:
            raise HTTPException(status_code=403, detail="You don’t have permission for this action")

        return current_user
    return role_checker
