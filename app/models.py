# app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    status = Column(String, nullable=False)  # "Lead", "Prospect", "Customer"
