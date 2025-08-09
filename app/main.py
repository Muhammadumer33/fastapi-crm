# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

# Create DB tables (only on startup / first run)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple CRM API", version="1.0")

# 1) CREATE
@app.post("/contacts", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

# 2) READ - ALL
@app.get("/contacts", response_model=List[schemas.ContactOut])
def read_contacts(db: Session = Depends(get_db), limit: int = Query(100, ge=1)):
    contacts = crud.get_all_contacts(db)
    return contacts[:limit]

# 2) READ - SINGLE
@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# 3) UPDATE (PUT/PATCH)
@app.patch("/contacts/{contact_id}", response_model=schemas.ContactOut)
@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, updates: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated = crud.update_contact(db, contact_id, updates)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return updated

# 4) DELETE
@app.delete("/contacts/{contact_id}", status_code=status.HTTP_200_OK)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"message": f"Contact {contact_id} deleted successfully"}

# 5) SEARCH
@app.get("/contacts/search", response_model=List[schemas.ContactOut])
def search_contacts(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    results = crud.search_contacts(db, q)
    return results
