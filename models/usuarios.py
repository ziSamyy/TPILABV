from config.database import Base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from models.prestamos import Lending


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(Enum("Librarian", "Client", name="rol_user"), nullable=False)

    lendings = relationship("Lending", back_populates="user")

