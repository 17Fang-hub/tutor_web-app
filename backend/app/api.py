from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db, Subject, Tutor, Booking
from . import schemas

router = APIRouter()

# ================= SUBJECTS =================
@router.post("/subjects/", response_model=schemas.SubjectOut)
async def create_subject(subject: schemas.SubjectCreate, db: AsyncSession = Depends(get_db)):
    new_subject = Subject(name=subject.name)
    db.add(new_subject)
    await db.commit()
    await db.refresh(new_subject)
    return new_subject

@router.get("/subjects/", response_model=list[schemas.SubjectOut])
async def get_subjects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subject))
    return result.scalars().all()

@router.delete("/subjects/{subject_id}")
async def delete_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    await db.delete(subject)
    await db.commit()
    return {"message": "Subject deleted"}

# ================= TUTORS =================
@router.post("/tutors/", response_model=schemas.TutorOut)
async def create_tutor(tutor: schemas.TutorCreate, db: AsyncSession = Depends(get_db)):
    # Перевіряємо, чи існує такий предмет
    subj_check = await db.execute(select(Subject).where(Subject.id == tutor.subject_id))
    if not subj_check.scalar_one_or_none():
         raise HTTPException(status_code=400, detail="Subject ID does not exist")
         
    new_tutor = Tutor(**tutor.model_dump())
    db.add(new_tutor)
    await db.commit()
    await db.refresh(new_tutor)
    return new_tutor

@router.get("/tutors/", response_model=list[schemas.TutorOut])
async def get_tutors(subject_id: int | None = None, db: AsyncSession = Depends(get_db)):
    query = select(Tutor)
    # Якщо передано subject_id, фільтруємо за ним
    if subject_id:
        query = query.where(Tutor.subject_id == subject_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/tutors/{tutor_id}")
async def delete_tutor(tutor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tutor).where(Tutor.id == tutor_id))
    tutor = result.scalar_one_or_none()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor not found")
    await db.delete(tutor)
    await db.commit()
    return {"message": "Tutor deleted"}

# ================= BOOKINGS =================
@router.post("/bookings/", response_model=schemas.BookingOut)
async def create_booking(booking: schemas.BookingCreate, db: AsyncSession = Depends(get_db)):
    new_booking = Booking(**booking.model_dump())
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking

@router.get("/bookings/", response_model=list[schemas.BookingOut])
async def get_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking))
    return result.scalars().all()