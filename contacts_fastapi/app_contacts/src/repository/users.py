from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.users import UserModel, UserUpdate
# from src


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def update_user(body: UserUpdate, user: User, db: Session) -> User:
    user.first_name = body.first_name
    user.last_name = body.last_name
    user.birthday = body.birthday
    user.job = body.job
   
    db.commit()
    db.refresh(user)
    return user


async def update_avatar(email: str, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
        
    new_user = User(**body.dict(), avatar=avatar, role_id=3)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
    
    
async def confirmed_email(user: User, db: Session) -> None:
    # user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    
    
async def save_new_password(user: User, password_hash, db: Session) -> None:
    # user = await get_user_by_email(email, db)
    user.password = password_hash
    db.commit()