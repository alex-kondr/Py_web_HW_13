from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User, Group
from src.schemas.contacts import ContactBase, ContactModel, ContactUpdate, ContactEmailUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()



async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contact_by_fields(first_name: str,
                               last_name: str,
                               phone: str,
                               email: str,
                               days_before_birth: int,
                               user: User,
                               db: Session) -> List[Contact]:
    
    contact = db.query(Contact)
    
    if first_name:
        contact = contact.filter(and_(Contact.first_name == first_name, Contact.user_id == user.id))
        
    if last_name:
        contact = contact.filter(and_(Contact.last_name == last_name, Contact.user_id == user.id))
    
    if phone:
        contact = contact.filter(and_(Contact.phone == phone, Contact.user_id == user.id))
        
    if email:
        contact = contact.filter(and_(Contact.email == email, Contact.user_id == user.id))        
    
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days_before_birth)     
    contact = contact.filter(and_(Contact.birthday.between(start_date, end_date), Contact.user_id == user.id))
    
    return contact.all()


async def create_contact(body: ContactBase, user: User, db: Session) -> Contact:
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    
    if contact:
        groups = db.query(Group).filter(and_(Group.id.in_(body.groups), Group.user_id == user.id)).all()
        
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.job = body.job
        contact.groups = groups
        db.commit()
        
    return contact


async def update_email_contact(contact_id: int, body: ContactEmailUpdate, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    
    if contact:
        contact.email = body.email
        db.commit()
        
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    
    if contact:
        db.delete(contact)
        db.commit()
        
    return contact