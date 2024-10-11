from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    is_active: Optional[bool] = True
    rfc: Optional[str] = None
    curp: Optional[str] = None
    cp: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
