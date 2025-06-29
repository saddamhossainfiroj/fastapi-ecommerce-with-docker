from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime

    class Config:
        orm_mode = True

class ProductCategory(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True

class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int = 0
    created_at: datetime
    updated_at: datetime | None = None
    is_active: bool = True

    class Config:
        orm_mode = True


