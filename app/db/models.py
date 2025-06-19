from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    register_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
