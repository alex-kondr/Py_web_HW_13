from datetime import datetime, date
from typing import Optional, Annotated

from pydantic import BaseModel, Field, EmailStr, constr
from fastapi import UploadFile, File, Form

class UserBase(BaseModel):
    password: Annotated[str, Form()]        


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Annotated[str, Form()]
    birthday: Optional[date]
    job: Optional[str]
    email: Annotated[EmailStr, Form()]
    avatar: Annotated[UploadFile, File()]
    phone: Optional[
        constr(
            strip_whitespace=True,
            regex=r"^(\+)[1-9][0-9\-\(\)]{9,18}$",
        )
    ]
    
    
class UserModel(UserBase, UserUpdate):
    pass

class UserDB(UserUpdate):
    id: int
    created_at: datetime
    avatar: Optional[str]
    
    class Config:
        orm_mode = True
        
        
class UserResponse(BaseModel):
    user: UserDB
    detail: str = "User seccessfully created"
    

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
    
    
class UpdatePassword(BaseModel):
    password: str = Field(min_length=6, max_length=10)