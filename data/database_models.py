from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional

engine = create_engine("postgresql+psycopg2://postgres:mysecretpassword@localhost:5433/classroom_db")

class Base(DeclarativeBase):
    pass
class AssignmentDB(Base):
    __tablename__= "assignments"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    courseId: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
# Change Optional[str] -> dict / list since they are JSON columns
    driveId: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    materials: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    # Use datetime instead of date if your due dates include hours/minutes (e.g., 2026-08-04 18:59)
    dueDate: Mapped[Optional[datetime]] = mapped_column(nullable=True)

AssignmentDB.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()