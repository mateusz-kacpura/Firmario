from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_company
from app.schemas.company import Company, CompanyCreate, CompanyUpdate, CompanyBranch, CompanyBranchCreate
from app.api.dependencies import get_db

router = APIRouter()

# --- Endpointy dla Firm ---

@router.get("/companies", response_model=List[Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Pobierz listę firm.
    """
    companies = crud_company.company.get_multi(db, skip=skip, limit=limit)
    return companies

@router.post("/companies", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    """
    Utwórz nową firmę.
    """
    return crud_company.company.create(db=db, obj_in=company_in)

@router.get("/companies/{company_id}", response_model=Company)
def read_company(company_id: int, db: Session = Depends(get_db)):
    """
    Pobierz firmę po ID.
    """
    db_company = crud_company.company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """
    Usuń firmę (wraz z jej oddziałami dzięki cascade).
    """
    db_company = crud_company.company.get(db, id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    crud_company.company.remove(db, id=company_id)
    return

# --- Endpointy dla Oddziałów Firm ---

@router.get("/companies/{company_id}/branches", response_model=List[CompanyBranch])
def read_company_branches(company_id: int, db: Session = Depends(get_db)):
    """
    Pobierz listę oddziałów dla konkretnej firmy.
    """
    db_company = crud_company.company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
        
    branches = crud_company.company_branch.get_multi_by_company(db, company_id=company_id)
    return branches

@router.post("/companies/{company_id}/branches", response_model=CompanyBranch, status_code=status.HTTP_201_CREATED)
def create_company_branch(company_id: int, branch_in: CompanyBranchCreate, db: Session = Depends(get_db)):
    """
    Utwórz nowy oddział dla konkretnej firmy.
    """
    db_company = crud_company.company.get(db, id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud_company.company_branch.create_with_company(db, obj_in=branch_in, company_id=company_id)

@router.delete("/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    """
    Usuń konkretny oddział.
    """
    branch = crud_company.company_branch.remove(db, id=branch_id)
    if not branch:
         raise HTTPException(status_code=404, detail="Branch not found")
    return