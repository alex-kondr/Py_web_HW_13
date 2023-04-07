from pathlib import Path

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")


engine = create_engine(env("SQLALCHEMY_DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    
    __tablename__ = "quotes_author"
    id = Column(Integer(), primary_key=True)    
    fullname = Column(String(250))
    born_date = Column(DateTime())
    born_location =Column(String())
    description = Column(Text())
    

class Quote(Base):
    
    __tablename__ = "quotes_quote"
    id = Column(Integer(), primary_key=True)
    tags = Column(String(500))
    author_id = Column(Integer(), ForeignKey("quotes_author.id"))
    author = relationship("Author")
    quote = Column(Text())