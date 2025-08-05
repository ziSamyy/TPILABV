from pydantic import Field, PositiveInt, ConfigDict, BaseModel
from datetime import datetime, timezone
from typing import Optional

def utc_now():
    return datetime.now(timezone.utc)

class Lending(BaseModel):
    id: Optional[PositiveInt] = None
    book_id: PositiveInt
    user_id: PositiveInt
    lending_date: Optional[datetime] = Field(default_factory=utc_now)
    return_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
        