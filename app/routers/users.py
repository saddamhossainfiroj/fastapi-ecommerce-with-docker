from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models
from ..database import SessionLocal
from sqlalchemy.future import select
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[schemas.User])
async def get_user(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    user = result.scalars().all()
    return user

@router.get("/{user_id}", response_model=schemas.User)
async def get_category(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Product not found")
    return user

@router.post("/", response_model=schemas.User)
async def create_category(user: schemas.User, db: AsyncSession = Depends(get_db)):
    user.created_at = datetime.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user