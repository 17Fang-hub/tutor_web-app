from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# --- Схеми для Subject ---
class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для Tutor ---
class TutorBase(BaseModel):
    full_name: str
    description: str
    price: float
    subject_id: int

class TutorCreate(TutorBase):
    pass

class TutorOut(TutorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для Booking ---
class BookingBase(BaseModel):
    tutor_id: int
    customer_name: str
    booking_date: datetime

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)