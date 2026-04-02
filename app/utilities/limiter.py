from jose import jwt, JWTError
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.services.tokenService import JWT_SECRET, JWT_ALG


def get_user_id_key(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
            return f"user:{payload['sub']}"
        except JWTError:
            pass
    return get_remote_address(request)


limiter = Limiter(key_func=get_user_id_key)
