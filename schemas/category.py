from typing import Optional
from pydantic import Field, ConfigDict, BaseModel, PositiveInt

class Category(BaseModel):
    id: Optional[PositiveInt] = None
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default="No description", max_length=255)

    model_config = ConfigDict(from_attributes=True)