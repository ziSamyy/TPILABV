from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.libros import Book



class Lending(Base):
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lending_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="lendings")
    user = relationship("User", back_populates="lendings")