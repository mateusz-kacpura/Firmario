# Plik: app/core/database.py

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} # Potrzebne tylko dla SQLite
)

# --- POCZĄTEK POPRAWKI ---
# Włącz wymuszanie kluczy obcych (foreign keys) dla SQLite
# To jest krytyczne dla integralności danych.
if "sqlite" in settings.DATABASE_URL:
    def _fk_pragma_on_connect(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        _fk_pragma_on_connect(dbapi_connection, connection_record)
# --- KONIEC POPRAWKI ---


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()