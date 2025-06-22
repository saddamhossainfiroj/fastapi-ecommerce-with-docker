from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at  = Column(DateTime, nullable=False)
    updated_at  = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<ProductCategory(id={self.id}, name={self.name})>"

class Product(Base):
    __tablename__ = 'products'

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price       = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    created_at  = Column(DateTime, nullable=False)
    updated_at  = Column(DateTime, nullable=True)
    is_active   = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"


