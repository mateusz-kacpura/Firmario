# Plik: app/api/endpoints/people.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud_person
from app.schemas.person import Person, PersonCreate, PersonUpdate, PersonInDB
from app.api.dependencies import get_db
from app.models import models

router = APIRouter()

# --- POCZĄTEK REFAKTORYZACJI ---
def enrich_person_data(person_db: models.Person) -> dict:
    """
    Pomocnicza funkcja, która konwertuje model SQLAlchemy na słownik,
    który zostanie użyty do zbudowania finalnej odpowiedzi JSON.
    """
    # Zacznij od danych bazowych z samego obiektu Person
    person_dict = PersonInDB.model_validate(person_db).model_dump()
    
    # Ręcznie dodaj dane z załadowanych relacji
    person_dict['miejscowosc'] = person_db.town.name if person_db.town else "Brak"
    if person_db.company_branch and person_db.company_branch.company:
        person_dict['firma'] = person_db.company_branch.company.name
        person_dict['oddzial_firmy'] = person_db.company_branch.name
        person_dict['company_id'] = person_db.company_branch.company.id # Dodano company_id
    else:
        person_dict['firma'] = "Brak"
        person_dict['oddzial_firmy'] = "Brak"
        person_dict['company_id'] = None # Dodano company_id
        
    # Schemat `Person` (response_model) automatycznie użyje tych danych do obliczenia `age` i `gender`.
    return person_dict

@router.get("/people", response_model=List[Person])
def read_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    people_db = crud_person.person.get_multi_details(db, skip=skip, limit=limit)
    return [enrich_person_data(p) for p in people_db]

@router.post("/people", response_model=Person, status_code=status.HTTP_201_CREATED)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    try:
        person_db = crud_person.person.create_and_get_details(db=db, obj_in=person)
        if not person_db:
             raise HTTPException(status_code=500, detail="Nie udało się utworzyć ani pobrać osoby.")
        return enrich_person_data(person_db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nie można utworzyć osoby. Upewnij się, że miejscowość o id={person.town_id} "
                   f"oraz oddział firmy o id={person.company_branch_id} istnieją."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Wystąpił nieoczekiwany błąd: {e}"
        )

@router.get("/people/{person_id}", response_model=Person)
def read_person(person_id: int, db: Session = Depends(get_db)):
    person_db = crud_person.person.get_details(db, id=person_id)
    if person_db is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return enrich_person_data(person_db)

@router.put("/people/{person_id}", response_model=Person)
def update_person(person_id: int, person_in: PersonUpdate, db: Session = Depends(get_db)):
    person_db_obj = crud_person.person.get(db, id=person_id)
    if not person_db_obj:
        raise HTTPException(status_code=404, detail="Person not found")
    
    crud_person.person.update(db, db_obj=person_db_obj, obj_in=person_in)
    updated_person_details = crud_person.person.get_details(db, id=person_id)
    if not updated_person_details:
        raise HTTPException(status_code=404, detail="Person not found after update")
        
    return enrich_person_data(updated_person_details)

@router.delete("/people/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person_db = crud_person.person.remove(db, id=person_id)
    if not person_db:
        raise HTTPException(status_code=404, detail="Person not found")
    return
# --- KONIEC REFAKTORYZACJI ---