from uuid import uuid4

from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import cloudinary.api

from src.conf.config import settings
from src.database.models import User

async def upload_avatar(file: UploadFile, name: str) -> str:
    cloudinary.config(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )
 
    cloudinary.uploader.upload(file.file, public_id=f"ContactsApp/{name}", overwrite=True,
                                eager = [{"width": 250, "height": 250, "crop": "fill"}])
    image_info=cloudinary.api.resource(f"ContactsApp/{name}")
    src_url = image_info["derived"][0]["secure_url"]
    return src_url