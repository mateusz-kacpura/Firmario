# People Management API

Prosta aplikacja API stworzona przy użyciu **FastAPI** do zarządzania listą osób, firm, oddziałów i miejscowości.

## Funkcjonalności

*   **Zarządzanie Osobami**: Tworzenie, odczytywanie, aktualizowanie i usuwanie danych osób.
*   **Dane Powiązane**: Zarządzanie firmami, ich oddziałami oraz miejscowościami.
*   **Logika Biznesowa**:
    *   Wiek osoby jest obliczany dynamicznie na podstawie daty urodzenia.
    *   Płeć jest automatycznie określana na podstawie końcówki imienia (`a` -> Kobieta, inne -> Mężczyzna).
*   **Testy Dymne**: Wbudowany system testów dymnych uruchamiany przy starcie aplikacji w celu weryfikacji kluczowych endpointów.
*   **Migracje Bazy Danych**: Zarządzanie schematem bazy danych przy użyciu **Alembic**.

## Struktura Projektu

Projekt jest zorganizowany w modułowy sposób, aby zapewnić czytelność i łatwość w utrzymaniu:

-   `/app`: Główny kod aplikacji.
    -   `/api`: Definicje endpointów API.
    -   `/core`: Konfiguracja, połączenie z bazą danych.
    -   `/crud`: Funkcje do operacji na bazie danych (Create, Read, Update, Delete).
    -   `/models`: Modele SQLAlchemy ORM.
    -   `/schemas`: Schematy Pydantic do walidacji i serializacji danych.
    -   `/smoke_tests`: Automatyczne testy dymne.
-   `/alembic`: Pliki konfiguracyjne dla migracji bazy danych.
-   `/scripts`: Skrypty pomocnicze (np. do uruchamiania aplikacji).

## Technologia

*   **Framework**: FastAPI
*   **Baza Danych**: SQLite (z możliwością łatwej zmiany na inną)
*   **ORM**: SQLAlchemy
*   **Migracje**: Alembic
*   **Walidacja Danych**: Pydantic

## Instalacja i Uruchomienie

### Wymagania

*   Python 3.8+

### Kroki

1.  **Sklonuj repozytorium:**
    ```bash
    git clone <URL_do_repozytorium>
    cd <nazwa_katalogu>
    ```

2.  **Utwórz i aktywuj wirtualne środowisko:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Na Windows: venv\Scripts\activate
    ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Skonfiguruj zmienne środowiskowe:**
    Skopiuj plik `.env.example` do `.env` i dostosuj go do swoich potrzeb. Domyślnie używana jest baza SQLite.
    ```bash
    cp .env.example .env
    ```

5.  **Uruchom migracje bazy danych:**
    ```bash
    alembic upgrade head
    ```

6.  **Uruchom aplikację:**
    Możesz użyć skryptu `run.sh`:
    ```bash
    chmod +x scripts/run.sh
    ./scripts/run.sh
    ```
    Lub uruchomić serwer `uvicorn` bezpośrednio:
    ```bash
    uvicorn main:app --reload
    ```
    Aplikacja będzie dostępna pod adresem `http://127.0.0.1:8000`.

7.  **Dokumentacja API:**
    Interaktywna dokumentacja Swagger UI jest dostępna pod adresem `http://127.0.0.1:8000/docs`.

## Uruchamianie Testów Dymnych

Testy dymne są domyślnie włączone i uruchamiają się przy starcie aplikacji. Możesz je wyłączyć, ustawiając flagę w pliku `.env`:

```env
RUN_SMOKE_TESTS=False
