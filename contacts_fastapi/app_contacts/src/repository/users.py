from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserModel, UserUpdate


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_phone(phone: str, db: Session) -> User:
    return db.query(User).filter(User.phone == phone).first()


async def update_user(body: UserUpdate, user: User, db: Session) -> User:
    user.first_name = body.first_name
    user.last_name = body.last_name
    user.birthday = body.birthday
    user.job = body.job
   
    db.commit()
    db.refresh(user)
    return user


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
        
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()