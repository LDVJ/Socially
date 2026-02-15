from .db import Base
from sqlalchemy import String, DateTime,func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True, nullable= False)
    name : Mapped[str] = mapped_column(String(250),nullable=False)
    email : Mapped[str] = mapped_column(String(250),nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String(250),nullable=False)
    username : Mapped[str] = mapped_column(String(150),nullable=False, unique=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    user_posts = relationship("Posts")


class Posts(Base):
    __tablename__ = "posts"

    id : Mapped[int] = mapped_column(nullable=True, primary_key= True)
    title : Mapped[str] = mapped_column(String(250), nullable=False)
    content : Mapped[str] = mapped_column(String(300))
    tags : Mapped[list]  = mapped_column(String(250),nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=True,onupdate=func.now())
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete ="CASCADE"), nullable=False)
