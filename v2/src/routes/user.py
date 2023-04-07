import pickle

from fastapi import APIRouter, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserResponse, UserUpdate, UserDB
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.upload_avatar import upload_avatar


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserDB)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch("/avatar", response_model=UserDB)
async def update_avatar_user(body: UserUpdate,
                             current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    
    url = await upload_avatar(body.avatar, f"Users/{current_user.username}")
    user = await repository_users.update_avatar(current_user.email, url, db)
    await auth_service.r.set(f"user:{user.email}", pickle.dumps(user), ex=7200)
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED,
            description="No more than 10 requests per minute",
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_profile(body: UserUpdate,
                  current_user: User = Depends(auth_service.get_current_user), 
                  db: Session = Depends(get_db)):
   
    user = await repository_users.update_user(body, current_user, db)
    return user