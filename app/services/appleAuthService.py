import os
import httpx
from jose import jwt, JWTError

APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"
# Set APPLE_CLIENT_ID in your environment to your app's bundle ID
APPLE_CLIENT_ID = os.getenv("APPLE_CLIENT_ID", "com.robertfusting.boardGameReview")


async def verify_apple_token(identity_token: str) -> dict:
    """Fetch Apple's public JWKS, find the matching key, and verify the token."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(APPLE_KEYS_URL)
        resp.raise_for_status()
        keys = resp.json()["keys"]

    header = jwt.get_unverified_header(identity_token)
    kid = header.get("kid")

    matching_key = next((k for k in keys if k["kid"] == kid), None)
    if not matching_key:
        raise ValueError("No matching Apple public key found for kid: " + str(kid))

    claims = jwt.decode(
        identity_token,
        matching_key,
        algorithms=["RS256"],
        audience=APPLE_CLIENT_ID,
        issuer=APPLE_ISSUER,
    )
    return claims
