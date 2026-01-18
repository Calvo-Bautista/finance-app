from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.utils.helpers import PyObjectId

# Esquema base (datos compartidos)
class UserBase(BaseModel):
    email: EmailStr
    nombre: str

# Esquema para crear usuario (entrada)
class UserCreate(UserBase):
    password: str

# Esquema para base de datos (interno)
class UserInDB(UserBase):
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Esquema de respuesta (salida - sin password)
class UserResponse(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# Esquema para Token
class Token(BaseModel):
    access_token: str
    token_type: str