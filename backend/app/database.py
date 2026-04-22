import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from datetime import datetime, timezone

# Завантажуємо змінні з .env файлу
load_dotenv(dotenv_path="../.env")

DATABASE_URL = os.getenv("DATABASE_URL")

# Явна перевірка: якщо змінної немає, викидаємо помилку
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set! Please check your .env file.")

# Тепер аналізатор коду точно знає, що тут DATABASE_URL є рядком (str)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # Зв'язок: один предмет має багато репетиторів
    tutors: Mapped[list["Tutor"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

class Tutor(Base):
    __tablename__ = "tutors"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    
    # Зв'язки
    subject: Mapped["Subject"] = relationship(back_populates="tutors")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="tutor", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutors.id"))
    customer_name: Mapped[str] = mapped_column(String)
    booking_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Зв'язки
    tutor: Mapped["Tutor"] = relationship(back_populates="bookings")

# Залежність для отримання сесії бази даних в ендпоінтах
async def get_db():
    async with async_session() as session:
        yield session