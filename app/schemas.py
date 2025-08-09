# app/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    Lead = "Lead"
    Prospect = "Prospect"
    Customer = "Customer"

class ContactBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    status: Optional[StatusEnum] = None

class ContactCreate(ContactBase):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    company: str
    status: StatusEnum

    # additional validation if needed
    @validator("phone_number")
    def phone_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("phone_number must not be empty")
        return v

class ContactUpdate(ContactBase):
    # all optional, used for PATCH/PUT partial updates
    pass

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
