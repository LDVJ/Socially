from ..db import Base
from sqlalchemy import String, DateTime,func, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from . import usersdb


class Posts(Base):
    __tablename__ = "posts"

    id : Mapped[int] = mapped_column(primary_key= True)
    title : Mapped[str] = mapped_column(String(250), nullable=False)
    content : Mapped[str] = mapped_column(String(300))
    tags : Mapped[list[str]]  = mapped_column(JSON,nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at : Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True,onupdate=func.now())
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete ="CASCADE"), nullable=False)
    owner: Mapped["usersdb.Users"] = relationship(back_populates="user_posts")

class PostLikes(Base):
    __tablename__ = "post_likes"

    id : Mapped[int] = mapped_column(primary_key=True)
    post_id : Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("post_id","user_id", name="user_post_like"),
    )

class PostComments(Base):
    __tablename__ = "post_comments"

    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)

    post_id : Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    content : Mapped[str] = mapped_column(String(500), nullable=False)

    comment_uid : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    parent_id : Mapped[int] = mapped_column(ForeignKey("post_comments.id",ondelete="CASCADE"), nullable=True)

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
