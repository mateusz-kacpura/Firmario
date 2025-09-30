import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.smoke_tests.utils import run_test_from_file

def run_test(client: TestClient) -> list:
    """
    Uruchamia testy dymne dla endpointów związanych z Osobami (People).
    """
    print("\n--- Rozpoczęcie testów dla: People ---")
    
    test_data_path = Path(__file__).parent.parent / "data" / "people.json"
    with open(test_data_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
        
    return run_test_from_file(client, test_data)