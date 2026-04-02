import os
from datetime import datetime, timedelta, timezone
from jose import jwt
import hashlib
import secrets

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = "HS256"

if os.getenv("JWT_SECRET"):
    print("JWT_SECRET loaded from environment")
else:
    print("WARNING: JWT_SECRET not set, using insecure fallback")

ACCESS_TTL_MIN = 15
REFRESH_TTL_DAYS = 60

def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TTL_MIN)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

def new_refresh_token() -> str:
    # raw token sent to client once
    return secrets.token_urlsafe(48)

def hash_refresh_token(raw: str) -> str:
    # store ONLY hash in DB
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

