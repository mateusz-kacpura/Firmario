# Plik: app/schemas/person.py

import datetime
from pydantic import BaseModel, Field, computed_field
from typing import Optional

class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, example="Anna")
    last_name: str = Field(..., min_length=1, example="Kowalska")
    birth_date: datetime.date = Field(..., example="1990-01-15")
    town_id: int = Field(..., gt=0, example=1)
    company_branch_id: int = Field(..., gt=0, example=1)

class PersonCreate(PersonBase):
    pass

class PersonUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    birth_date: Optional[datetime.date] = None
    town_id: Optional[int] = Field(None, gt=0)
    company_branch_id: Optional[int] = Field(None, gt=0)

class PersonInDB(PersonBase):
    id: int

    class Config:
        from_attributes = True

class Person(PersonInDB):
    miejscowosc: str
    firma: str
    oddzial_firmy: str

    @computed_field
    @property
    def age(self) -> int:
        today = datetime.date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @computed_field
    @property
    def gender(self) -> str:
        return "Kobieta" if self.first_name.lower().endswith('a') else "Mężczyzna"

    company_id: Optional[int] = None
