from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserResponse, UserUpdate
from src.repository import users as repository_users
from src.services.auth import auth_service


router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_profile(body: UserUpdate, 
                  current_user: User = Depends(auth_service.get_current_user), 
                  db: Session = Depends(get_db)):
   
    user = await repository_users.update_user(body, current_user, db)
    return user