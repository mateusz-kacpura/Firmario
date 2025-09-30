# Plik: app/smoke_tests/utils.py

import json
import re
from fastapi.testclient import TestClient
from typing import Dict, Any

# === PALETA KOLORÓW ===
GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"
BOLD = "\033[1m"
GRAY = "\033[90m"

METHOD_COLORS = {
    "GET": "\033[96m", "POST": "\033[92m", "PUT": "\033[93m", "DELETE": "\033[91m",
}


def format_payload(payload_template: Any, captured_ids: Dict[str, Any]) -> Any:
    """
    Rekursywnie formatuje stringi w szablonie payloadu, używając captured_ids.
    Unika błędu formatowania całego stringu JSON.
    """
    if isinstance(payload_template, dict):
        return {k: format_payload(v, captured_ids) for k, v in payload_template.items()}
    elif isinstance(payload_template, list):
        return [format_payload(i, captured_ids) for i in payload_template]
    elif isinstance(payload_template, str):
        try:
            # Formatuj tylko, jeśli to string
            return payload_template.format(**captured_ids)
        except KeyError:
            # Jeśli string zawiera '{' ale nie jako placeholder, zwróć oryginał
            return payload_template
    else:
        # Zwróć inne typy (int, bool, etc.) bez zmian
        return payload_template


def get_outcome_description(status: int) -> str:
    """Zwraca opis oczekiwanego wyniku na podstawie kodu statusu."""
    if status < 300: return f"{GREEN}(oczekiwany sukces){RESET}"
    if 400 <= status < 500: return f"{YELLOW}(oczekiwany błąd klienta){RESET}"
    return f"{RED}(oczekiwany błąd serwera){RESET}"

def run_test_from_file(client: TestClient, test_data: Dict[str, Any]) -> list:
    """Uruchamia serię testów zdefiniowanych w słowniku (wczytanym z JSON)."""
    results = []
    captured_ids = {}

    METHOD_URL_WIDTH = 50
    DESCRIPTION_WIDTH = 75

    for test in test_data["tests"]:
        opis = test["opis"]
        method = test["method"]
        path_template = test["path"]
        expected_status = test["oczekiwany_status"]
        payload_template = test.get("payload")

        # --- POCZĄTEK ZMIAN DIAGNOSTYCZNYCH ---
        print(f"--- DEBUG: Uruchamianie testu '{opis}'. Obecne ID: {captured_ids}")
        # --- KONIEC ZMIAN DIAGNOSTYCZNYCH ---
        
        # Formatowanie ścieżki i payloadu z przechwyconymi ID
        path = path_template.format(**captured_ids)
        payload = format_payload(payload_template, captured_ids) if payload_template else None

        method_color = METHOD_COLORS.get(method.upper(), "")
        colored_method = f"{method_color}[{method.upper()}]{RESET}"
        
        endpoint_str_raw = f"[{method.upper()}] {path}"
        endpoint_str_colored = f"{colored_method} {path}"
        padding1 = " " * (METHOD_URL_WIDTH - len(endpoint_str_raw))

        outcome_desc = get_outcome_description(expected_status)
        full_opis_raw = f"Test: '{opis}' {outcome_desc}"
        full_opis_colored = f"Test: '{opis}' {outcome_desc}"
        padding2 = " " * (DESCRIPTION_WIDTH - len(full_opis_raw) + len(outcome_desc) - len(re.sub(r'\x1b\[[0-9;]*m', '', outcome_desc)))

        result_line_prefix = f"{endpoint_str_colored}{padding1}| {full_opis_colored}{padding2}"

        try:
            response = client.request(method, path, json=payload)
            
            if response.status_code == expected_status:
                result_line = f"{result_line_prefix} -> {GREEN}SUKCES{RESET} (Otrzymano: {response.status_code})"
                if "capture_id" in test and response.status_code < 300 and response.content:
                    try:
                        response_json = response.json()
                        if "id" in response_json:
                             # --- POCZĄTEK ZMIAN DIAGNOSTYCZNYCH ---
                             print(f"--- DEBUG: Przechwycono ID! Klucz: '{test['capture_id']}', Wartość: {response_json['id']}")
                             # --- KONIEC ZMIAN DIAGNOSTYCZNYCH ---
                             captured_ids[test["capture_id"]] = response_json["id"]
                        else:
                             # --- POCZĄTEK ZMIAN DIAGNOSTYCZNYCH ---
                             print(f"--- DEBUG: BŁĄD PRZECHWYTYWANIA! W odpowiedzi JSON nie ma klucza 'id'. Otrzymano: {response_json}")
                             # --- KONIEC ZMIAN DIAGNOSTYCZNYCH ---
                    except json.JSONDecodeError:
                        pass # Ignoruj jeśli odpowiedź nie jest JSONem
            else:
                failure_reason = f"Oczekiwano: {expected_status}, Otrzymano: {response.status_code}"
                result_line = f"{result_line_prefix} -> {RED}PORAŻKA{RESET} ({failure_reason})"

        except Exception as e:
            result_line = f"{result_line_prefix} -> {RED}EXCEPTION: {e}{RESET}"
        
        results.append({"line": result_line, "status": expected_status})
            
    return results