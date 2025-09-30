from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.models import Company, CompanyBranch
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyBranchCreate, CompanyBranchUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    pass

class CRUDCompanyBranch(CRUDBase[CompanyBranch, CompanyBranchCreate, CompanyBranchUpdate]):
    def create_with_company(self, db: Session, *, obj_in: CompanyBranchCreate, company_id: int) -> CompanyBranch:
        """
        Tworzy oddział przypisany do konkretnej firmy.
        """
        db_obj = self.model(**obj_in.model_dump(), company_id=company_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_company(self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100) -> list[CompanyBranch]:
        """
        Pobiera listę oddziałów dla konkretnej firmy.
        """
        return (
            db.query(self.model)
            .filter(self.model.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

company = CRUDCompany(Company)
company_branch = CRUDCompanyBranch(CompanyBranch)