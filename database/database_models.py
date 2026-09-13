from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, Enum
from datetime import datetime
from typing import Optional, Literal
from dotenv import load_dotenv
from sqlalchemy import String, DateTime, Text  # SQLAlchemy database types
load_dotenv()

engine = create_async_engine("postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/classroom.ai",echo=True)


class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

from typing import Optional, Literal
from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

Base = declarative_base()

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
        
    # Relationship back to AssignmentDB
    assignments: Mapped[list["AssignmentDB"]] = relationship("AssignmentDB", back_populates="course", cascade="all, delete-orphan")
    # Relationship back to UserCourses
    user_enrollments: Mapped[list["UserCourses"]] = relationship("UserCourses", back_populates="course", cascade="all, delete-orphan")


class AssignmentDB(Base):
    __tablename__ = "assignments"
    
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    
    # Foreign Key pointing to courses.id
    course_id: Mapped[str] = mapped_column(String(50), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    
    coursename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    materials: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    dueDate: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    due_date_status: Mapped[Literal["Pending", "Due", "WithoutDueDate"]] = mapped_column(String(50))

    # Relationship back to CourseDB
    course: Mapped["CourseDB"] = relationship("CourseDB", back_populates="assignments")


class UserCourses(Base):
    __tablename__ = "user_courses"
    # Using composite primary key so user cant be enrolled in same course twice!
    user_id: Mapped[str] = mapped_column(String(100), nullable=False ,primary_key=True)  # Tracks the Supabase user UUID
    
    # Foreign Key pointing to courses.id 
    course_id: Mapped[str] = mapped_column(String(50), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, primary_key=True)

    # Relationship back to CourseDB
    course: Mapped["CourseDB"] = relationship("CourseDB", back_populates="user_enrollments")

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,

)
session = AsyncSessionLocal()