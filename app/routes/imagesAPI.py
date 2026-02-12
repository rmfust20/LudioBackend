import os
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContentSettings

router = APIRouter(
    prefix="/images",
    )

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 8 * 1024 * 1024  # 8 MB

def blob_service_client() -> BlobServiceClient:
    account_name = "tabulususerimages"
    account_url = f"https://{account_name}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=account_url, credential=credential)

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    user_id: int = 1,
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(415, f"Unsupported content type: {file.content_type}")

    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File too large (max 8MB).")

    container_name = "images"

    # Choose a deterministic-ish path you can store in DB
    ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[file.content_type]
    blob_name = f"users/{user_id}/{uuid.uuid4().hex}.{ext}"

    bsc = blob_service_client()
    blob_client = bsc.get_blob_client(container=container_name, blob=blob_name)

    # Important: set Content-Type so browsers/clients treat it as an image
    # (otherwise it can default to application/octet-stream) :contentReference[oaicite:3]{index=3}
    blob_client.upload_blob(
        data,
        overwrite=False,
        content_settings=ContentSettings(content_type=file.content_type),
    )

    # Store blob_name in Postgres; return it to client for later retrieval
    return {"blob_name": blob_name}
