from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema para crear un nuevo administrador
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    is_active: Optional[bool] = True

# Esquema para actualizar un administrador
class AdminUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

# Esquema para devolver los detalles de un administrador
class AdminOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True
