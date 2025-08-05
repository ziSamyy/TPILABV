from typing import Optional
from pydantic import Field, ConfigDict, BaseModel, PositiveInt, HttpUrl  
from schemas.category import Category

class Book(BaseModel):
    id: Optional[PositiveInt] = None
    title: str = Field(max_length=255)
    author: Optional[str] = Field(default="Unknown", max_length=100)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r'^\d{13}$')
    publisher: Optional[str] = Field(default="Unknown", max_length=100)
    category_id: int
    amount: int = Field(default=1, ge=0, le=1, description="Amount: 0 o 1")
    image: Optional[str] = Field(default=None, max_length=255)



    model_config = ConfigDict(from_attributes=True)

class BookWithCategory(Book):
    categoria: Category