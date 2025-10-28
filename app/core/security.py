from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import bcrypt
import hashlib
from app.core.config import settings

def _prehash_password(password: str) -> bytes:
    """Pre-hash password with SHA-256 → 32 raw bytes (well under 72)."""
    return hashlib.sha256(password.encode("utf-8")).digest()

def get_password_hash(password: str) -> str:
    prehashed = _prehash_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(prehashed, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = _prehash_password(plain_password)
    return bcrypt.checkpw(prehashed, hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = _prehash_password(plain_password)
    return bcrypt.checkpw(prehashed, hashed_password.encode("utf-8"))