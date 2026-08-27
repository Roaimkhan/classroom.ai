from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, Enum
from datetime import datetime
from typing import Optional, Literal

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
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    materials: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    dueDate: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    due_date_status:Mapped[Literal["Pending", "Due", "WithoutDueDate"]] = mapped_column()


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,

)
session = AsyncSessionLocal()