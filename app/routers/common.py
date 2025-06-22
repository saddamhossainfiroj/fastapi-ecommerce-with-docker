from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models
from ..database import SessionLocal
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(prefix="/common", tags=["common"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[schemas.ProductCategory])
async def get_category(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ProductCategory))
    products_category = result.scalars().all()
    return products_category

@router.get("/{category_id}", response_model=schemas.ProductCategory)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.ProductCategory).where(models.ProductCategory.id == category_id))
    products_category = result.scalar_one_or_none()
    if not products_category:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_category

@router.post("/", response_model=schemas.ProductCategory)
async def create_category(category: schemas.ProductCategory, db: AsyncSession = Depends(get_db)):
    category.created_at = datetime.strptime(str(category.created_at), "%Y-%m-%d %H:%M:%S")
    category.updated_at = datetime.strptime(str(category.updated_at), "%Y-%m-%d %H:%M:%S")
    new_category = models.ProductCategory(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category