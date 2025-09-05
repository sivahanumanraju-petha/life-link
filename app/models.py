
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr

class DonorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    blood_type: str
    latitude: float
    longitude: float
    last_donated: Optional[datetime] = None
    available: bool = True

    @validator("blood_type")
    def uppercase_blood(cls, v):
        return v.upper()

class DonorOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str]
    blood_type: str
    location: dict
    last_donated: Optional[datetime]
    available: bool

class EmergencyRequestCreate(BaseModel):
    needed_blood_type: str
    latitude: float
    longitude: float
    units: int = 1
    note: Optional[str]

    @validator("needed_blood_type")
    def uppercase_blood(cls, v):
        return v.upper()
