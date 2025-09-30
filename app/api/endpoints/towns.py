from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud_town
from app.schemas.town import Town, TownCreate, TownUpdate
from app.api.dependencies import get_db

router = APIRouter()

@router.get("/towns", response_model=List[Town])
def read_towns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Pobierz listę miejscowości.
    """
    towns = crud_town.town.get_multi(db, skip=skip, limit=limit)
    return towns


@router.post("/towns", response_model=Town, status_code=status.HTTP_201_CREATED)
def create_town(town_in: TownCreate, db: Session = Depends(get_db)):
    """
    Utwórz nową miejscowość.
    """
    # --- POCZĄTEK POPRAWKI ---
    try:
        town = crud_town.town.create(db=db, obj_in=town_in)
        return town
    except IntegrityError:
        db.rollback() # Wycofaj transakcję, aby sesja była czysta
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Miejscowość o nazwie '{town_in.name}' już istnieje.",
        )

@router.get("/towns/{town_id}", response_model=Town)
def read_town(town_id: int, db: Session = Depends(get_db)):
    """
    Pobierz miejscowość po ID.
    """
    db_town = crud_town.town.get(db, id=town_id)
    if db_town is None:
        raise HTTPException(status_code=404, detail="Town not found")
    return db_town

@router.put("/towns/{town_id}", response_model=Town)
def update_town(town_id: int, town_in: TownUpdate, db: Session = Depends(get_db)):
    """
    Zaktualizuj miejscowość.
    """
    db_town = crud_town.town.get(db, id=town_id)
    if not db_town:
        raise HTTPException(status_code=404, detail="Town not found")
    town = crud_town.town.update(db, db_obj=db_town, obj_in=town_in)
    return town

@router.delete("/towns/{town_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_town(town_id: int, db: Session = Depends(get_db)):
    """
    Usuń miejscowość.
    """
    db_town = crud_town.town.get(db, id=town_id)
    if not db_town:
        raise HTTPException(status_code=404, detail="Town not found")
    crud_town.town.remove(db, id=town_id)
    return