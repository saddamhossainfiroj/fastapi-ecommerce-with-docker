from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import products, common, users
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://postgresql://ecommerce_db:stmCyGjsnqbMSAOTFwpQnIj2xd0nf8ce@dpg-d1bu41p5pdvs73e8gbp0-a/ecommerce_db_wmyj"
engine = create_async_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    retries = 5
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database initialized successfully")
            break
        except Exception as e:
            print(f"❌ DB connection failed (attempt {i+1}/{retries}): {e}")
            await asyncio.sleep(5)
    else:
        raise RuntimeError("❌ Failed to connect to DB after retries")

    yield  # App runs during this time

    # On shutdown (optional cleanup)
    await engine.dispose()
    print("🔻 Database engine disposed")

# ✅ Use lifespan in app
app = FastAPI(lifespan=lifespan)

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(common.router)
