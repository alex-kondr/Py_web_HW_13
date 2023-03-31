from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
import cloudinary.api
from src.conf.config import settings

async def upload_avatar(file: UploadFile, name: str) -> str:
    cloudinary.config(
            cloud_name=settings.cloudinary_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True
        )
 
    await cloudinary.uploader.upload(file.file, public_id=f"ContactsApp/{name}", overwrite=True,
                                eager = [{"width": 250, "height": 250, "crop": "fill"}])
    image_info = await cloudinary.api.resource(f"ContactsApp/{name}")
    src_url = image_info["derived"][0]["secure_url"]
    return src_url

def default_avatar():
    url = "https://res.cloudinary.com/diqkjtgls/image/upload/c_fill,w_250/v1680233623/ContactsApp/default.jpg"
    return url