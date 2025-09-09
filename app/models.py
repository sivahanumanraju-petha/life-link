
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Union
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
    last_donated: str
    available: bool = True
    @validator("blood_type")
    def uppercase_blood(cls, v):
        return v.upper()

class DonorOut(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    blood_type: str
    last_donated: str  # keep as string instead of date
    available: Union[bool, str]  # accept both

class EmergencyRequestCreate(BaseModel):
    needed_blood_type: str
    units: int = 1
    note: Optional[str]

    @validator("needed_blood_type")
    def uppercase_blood(cls, v):
        return v.upper()
