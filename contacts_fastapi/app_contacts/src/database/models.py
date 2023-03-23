from sqlalchemy import Column, Integer, String, func, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


contact_m2m_group = Table(
    "contact_m2m_group",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("contact_id", Integer, ForeignKey("contacts.id", ondelete="Cascade")),
    Column("group_id", Integer, ForeignKey("groups.id", ondelete="Cascade")),
)


class Contact(Base):    
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(18), nullable=False, unique=True)
    email = Column(String(255), unique=True, nullable=True, default=None)
    birthday = Column(Date)
    job = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    groups = relationship("Group", secondary=contact_m2m_group, backref="contacts")
    user_id = Column(ForeignKey("users.id", ondelete="Cascade"), default=None)
    user = relationship("User", backref="contacts")
    
    
class Group(Base):
    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="unique_group_user"),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="Cascade"), default=None)
    user = relationship("User", backref="groups")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True)
    phone = Column(String(18))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    birthday = Column(Date)
    job = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255))
    refresh_token = Column(String(255))