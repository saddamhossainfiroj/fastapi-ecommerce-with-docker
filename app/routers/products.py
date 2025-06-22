from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models
from ..database import SessionLocal
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(prefix="/products", tags=["products"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[schemas.Product])
async def get_products(db: AsyncSession = Depends(get_db)):
    print("Fetching active products")
    result = await db.execute(select(models.Product).where(models.Product.is_active == True))
    products = result.scalars().all()
    return products

@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id, models.Product.is_active == True))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.Product)
async def create_product(product: schemas.Product, db: AsyncSession = Depends(get_db)):
    product.created_at = datetime.strptime(str(product.created_at), "%Y-%m-%d %H:%M:%S")
    product.updated_at = datetime.strptime(str(product.updated_at), "%Y-%m-%d %H:%M:%S")
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product