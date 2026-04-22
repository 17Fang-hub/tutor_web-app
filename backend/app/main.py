from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base
from .api import router

# Lifespan подія для створення таблиць при старті сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Автоматично створює таблиці на основі моделей (для розробки)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закриває з'єднання при вимкненні
    await engine.dispose()

app = FastAPI(title="Tutor Finder API", lifespan=lifespan)

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У продакшені замініть на точний URL фронтенду
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо наші маршрути
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Backend is running. API documentation available at /docs"}