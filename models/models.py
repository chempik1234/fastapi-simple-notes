from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from .database import Base


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    # date_created = Column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    # author: Mapped[User] = relationship("User", lazy="joined", back_populates="notes")

    # def __repr__(self) -> str:
    #     return ""
    #     return f"Note ({self.id}) user id: {self.user_id}"


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(250))
# : Mapped[List["Note"]]
    # notes: Mapped[List[Note]] = relationship("Note", back_populates="author")

    # def __repr__(self) -> str:
    #     return ""
    #     return f"User ({self.id}) login: {self.login} encrypted password: {self.password}"
