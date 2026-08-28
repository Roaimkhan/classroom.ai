from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, Enum
from datetime import datetime
from typing import Optional, Literal
from dotenv import load_dotenv
from sqlalchemy import String, DateTime, Text  # SQLAlchemy database types
load_dotenv()

engine = create_async_engine("postgresql+asyncpg://postgres:mysecretpassword@localhost:5433/classroom_db",echo=True)


class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class AssignmentDB(Base):
    __tablename__= "assignments"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    courseId: Mapped[str] = mapped_column()
    coursename:Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    materials: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    dueDate: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    due_date_status:Mapped[Literal["Pending", "Due", "WithoutDueDate"]] = mapped_column()

class CourseDB(Base):
    __tablename__ = "courses"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    section: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    room: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    course_state: Mapped[str] = mapped_column(String(50), default="ACTIVE", nullable=False)
    alternate_link: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    calendar_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    course_group_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    creation_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,

)
session = AsyncSessionLocal()