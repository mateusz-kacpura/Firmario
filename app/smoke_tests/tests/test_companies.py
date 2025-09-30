import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.smoke_tests.utils import run_test_from_file

def run_test(client: TestClient) -> list:
    """
    Uruchamia testy dymne dla endpointów związanych z firmami i ich oddziałami (Companies & Branches).
    """
    print("\n--- Rozpoczęcie testów dla: Companies & Branches ---")
    
    test_data_path = Path(__file__).parent.parent / "data" / "companies.json"
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
        
    return run_test_from_file(client, test_data)