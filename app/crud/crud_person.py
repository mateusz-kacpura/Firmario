# Plik: app/crud/crud_person.py

from sqlalchemy.orm import Session, joinedload
from .base import CRUDBase
from app.models.models import Person, CompanyBranch
from app.schemas.person import PersonCreate, PersonUpdate

class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    # --- POCZĄTEK NOWEGO KODU ---
    def create_and_get_details(self, db: Session, *, obj_in: PersonCreate) -> Person | None:
        """
        Tworzy osobę, a następnie od razu pobiera ją z bazy
        wraz z załadowanymi relacjami.
        """
        # Użyj metody create z klasy bazowej
        created_person = super().create(db=db, obj_in=obj_in)
        # Użyj metody get_details z tej klasy, aby pobrać pełny obiekt
        return self.get_details(db=db, id=created_person.id)
    # --- KONIEC NOWEGO KODU ---

    def get_multi_details(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[Person]:
        return (
            db.query(self.model)
            .options(
                joinedload(Person.town),
                joinedload(Person.company_branch).joinedload(CompanyBranch.company)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_details(self, db: Session, id: int) -> Person | None:
        return (
            db.query(self.model)
            .options(
                joinedload(Person.town),
                joinedload(Person.company_branch).joinedload(CompanyBranch.company)
            )
            .filter(self.model.id == id)
            .first()
        )

person = CRUDPerson(Person)