# Plik: main.py

import uvicorn
from fastapi import FastAPI
# Zaktualizowane importy
from app.api.endpoints import people, companies, towns 
from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models import models
from app.smoke_tests.runner import run_all_smoke_tests
from app.crud.init_db import initialise_db

# Utworzenie tabel w bazie danych
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Dołączenie wszystkich routerów
app.include_router(people.router, prefix=settings.API_V1_STR, tags=["People"])
app.include_router(companies.router, prefix=settings.API_V1_STR, tags=["Companies & Branches"]) # Zmieniono tag dla lepszej organizacji
app.include_router(towns.router, prefix=settings.API_V1_STR, tags=["Towns"])


@app.on_event("startup")
def on_startup():
    """
    Zdarzenie wykonywane przy starcie aplikacji.
    """
    db = SessionLocal()
    # Inicjalizacja bazy danych podstawowymi danymi
    initialise_db(db)
    db.close()

    # Uruchomienie testów dymnych, jeśli flaga jest ustawiona
    if settings.RUN_SMOKE_TESTS:
        print("--- Uruchamianie testów dymnych przy starcie aplikacji ---")
        run_all_smoke_tests(app)
        print("--- Zakończono testy dymne ---")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the People Management API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)