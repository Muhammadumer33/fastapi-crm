# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from . import models, schemas

def create_contact(db: Session, contact_in: schemas.ContactCreate):
    # check unique email
    existing = db.query(models.Contact).filter(models.Contact.email == contact_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    db_contact = models.Contact(
        first_name=contact_in.first_name.strip(),
        last_name=contact_in.last_name.strip(),
        email=contact_in.email,
        phone_number=contact_in.phone_number.strip(),
        company=contact_in.company.strip(),
        status=contact_in.status.value if isinstance(contact_in.status, schemas.StatusEnum) else contact_in.status
    )
    db.add(db_contact)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create contact (integrity error)")
    db.refresh(db_contact)
    return db_contact

def get_all_contacts(db: Session):
    return db.query(models.Contact).order_by(models.Contact.id).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, updates: schemas.ContactUpdate):
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return None

    update_data = updates.dict(exclude_unset=True)

    # prevent setting email to already-existing email
    if "email" in update_data and update_data["email"] is not None:
        other = db.query(models.Contact).filter(models.Contact.email == update_data["email"], models.Contact.id != contact_id).first()
        if other:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already used by another contact")

    for key, value in update_data.items():
        # if update is an enum instance or string, set string
        if key == "status" and value is not None:
            # value might be enum member or string
            if isinstance(value, schemas.StatusEnum):
                setattr(contact, key, value.value)
            else:
                setattr(contact, key, str(value))
        elif value is not None:
            setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact_by_id(db, contact_id)
    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return contact

def search_contacts(db: Session, query: str):
    q = f"%{query}%"
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(q)) |
        (models.Contact.last_name.ilike(q)) |
        (models.Contact.email.ilike(q))
    ).all()
