# libros.py
from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from models.categorias import Category


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False, default="Unknown")
    isbn = Column(String(13), unique=True, index=True, nullable=False)
    publisher = Column(String(100), nullable=False, default="Unknown")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(SmallInteger, nullable=False, default=1)
    image = Column(String(255), nullable=True)


    category = relationship("Category", back_populates="books")
    lendings = relationship("Lending", back_populates="book")