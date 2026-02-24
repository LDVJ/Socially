from ..db import Base
from sqlalchemy import String, DateTime,func, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from . import postsdb



class Users(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True, nullable= False)
    name : Mapped[str] = mapped_column(String(250),nullable=False)
    email : Mapped[str] = mapped_column(String(250),nullable=False, unique=True, index=True)
    password : Mapped[str] = mapped_column(String(250),nullable=False)
    username : Mapped[str] = mapped_column(String(150),nullable=False, unique=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    user_posts :Mapped[list["postsdb.Posts"]]= relationship(back_populates="owner")
    # mob_number : Mapped[str] = mapped_column(String(15), nullable=True)


    
class FollowList(Base):
    __tablename__ = "follow_list"

    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)

    followed_uid : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    follower_uid : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index= True)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    __table_args__ = (
        UniqueConstraint("followed_uid", "follower_uid", name="followers_unique"),
    )