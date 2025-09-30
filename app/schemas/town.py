from pydantic import BaseModel
from typing import Optional

class TownBase(BaseModel):
    name: str

class TownCreate(TownBase):
    pass

class TownUpdate(BaseModel):
    name: Optional[str] = None

class Town(TownBase):
    id: int

    class Config:
        from_attributes = True