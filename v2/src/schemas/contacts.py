from datetime import datetime, date
from typing import List, Optional, Annotated, Union

from pydantic import BaseModel, Field, EmailStr, constr
from fastapi import UploadFile, File, Form

# from src.database.models import Group, User
from src.schemas.groups import GroupResponse
from src.schemas.users import UserModel


class ContactBase(BaseModel):
  first_name: Annotated[str, Form()]
  last_name: Annotated[str, Form()]
  avatar: Annotated[UploadFile, File()]
      
        
class ContactModel(ContactBase):
  email: Optional[EmailStr]
  birthday: Optional[date]
  job: Optional[str]
  # groups: Optional[List[int]]
  # groups: None = None
  phone: Optional[
      constr(
          strip_whitespace=True,
          regex=r"^(\+)[1-9][0-9\-\(\)]{9,16}$",
      )
  ]


class ContactResponse(BaseModel):
  id: int
  first_name: str
  last_name: str
  avatar: str
  email: Optional[EmailStr]
  birthday: Optional[date]
  job: Optional[str]
  # groups: Optional[List[int]]
  # groups: None = None
  created_at: datetime
  phone: Optional[
      constr(
          strip_whitespace=True,
          regex=r"^(\+)[1-9][0-9\-\(\)]{9,16}$",
      )
  ]
  detail: str = "Contact seccessfully created"
  
  class Config:
    orm_mode = True
    
    
class ContactAvatarUpdate(BaseModel):
    avatar: Annotated[UploadFile, File()]


class ContactEmailUpdate(BaseModel):
    email: Optional[EmailStr]
    

class ContactResponse1(BaseModel):
  # contact: ContactDB
  detail: str = "Contact seccessfully created"