from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Date
from datetime import date
from typing import Optional

engine = create_engine()

class Assignments(DeclarativeBase):
    __tablename__= "assignments"

    id : Mapped[str] = mapped_column(primary_key=True)
    courseId  : Mapped[str] = mapped_column()
    title  : Mapped[str] = mapped_column()
    description : Mapped[str] = mapped_column()
    driveId : Mapped[str] = mapped_column()
    dueDate : Mapped[Optional[date]] = mapped_column(Date)
    materials : Mapped[str] = mapped_column()

