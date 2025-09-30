from pydantic import BaseModel
from typing import List, Optional

# Schematy dla Oddziału Firmy
class CompanyBranchBase(BaseModel):
    name: str

class CompanyBranchCreate(CompanyBranchBase):
    pass

class CompanyBranchUpdate(BaseModel):
    name: Optional[str] = None

class CompanyBranch(CompanyBranchBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True

# Schematy dla Firmy
class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None

class Company(CompanyBase):
    id: int
    branches: List[CompanyBranch] = []

    class Config:
        from_attributes = True