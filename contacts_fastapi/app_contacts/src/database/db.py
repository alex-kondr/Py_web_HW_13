# import configparser
# from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings


# path = Path(__file__).parent
# config = configparser.ConfigParser()
# config.read(path.joinpath("config.ini"))
# db_url = config.get("DB", "url")
db_url = settings.sqlalchemy_database_url
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()