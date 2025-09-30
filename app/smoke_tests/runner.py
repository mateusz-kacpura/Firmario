import importlib
import sys
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.core.config import settings
from .utils import get_outcome_description, GREEN, RED, YELLOW, RESET, BOLD, GRAY

def setup_test_environment(client: TestClient) -> bool:
    """
    Przygotowuje środowisko testowe - w tym przypadku nie jest wymagane
    żadne specjalne przygotowanie, ponieważ dane są ładowane przy starcie.
    """
    print("--- Środowisko testowe gotowe (dane inicjalizowane przy starcie) ---")
    return True

def cleanup_test_environment() -> bool:
    """
    Sprzątanie po testach - w tym projekcie nie jest wymagane.
    """
    print(f"\n--- Sprzątanie nie jest wymagane ---")
    return True

def run_all_smoke_tests(app: FastAPI):
    print(f"\n{BOLD}--- URUCHAMIANIE MODUŁOWYCH TESTÓW DYMNYCH ---{RESET}")
    client = TestClient(app)
    
    if not setup_test_environment(client):
        return

    total_passed, total_failed = 0, 0
    all_results = []
    
    tests_path = Path(__file__).parent / "tests"
    sys.path.insert(0, str(tests_path.parent.parent.parent))

    for p in sorted(tests_path.glob("test_*.py")):
        module_path = ".".join(p.relative_to(Path.cwd()).parts).replace(".py", "")
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, "run_test"):
                test_results = module.run_test(client)
                for res in test_results:
                    all_results.append(res)
                    if "SUKCES" in res["line"]:
                        total_passed += 1
                    else:
                        total_failed += 1
        except Exception as e:
            import traceback
            print(f"{RED}BŁĄD importu/uruchomienia testu {p.name}: {e}\n{traceback.format_exc()}{RESET}")
            total_failed += 1
    
    header = " Wyniki testów "
    print(f"\n\n{BOLD}╭{'─' * (len(header) + 2)}╮{RESET}")
    print(f"{BOLD}│ {YELLOW}{header.upper()}{RESET} │{RESET}")
    print(f"{BOLD}╰{'─' * (len(header) + 2)}╯{RESET}")
    
    for line in [r['line'] for r in all_results]:
        print(f"    {GRAY}├─>{RESET} {line}")

    if not cleanup_test_environment():
        total_failed += 1

    summary_width = 46
    print(f"\n\n{BOLD}╭{'─' * summary_width}╮{RESET}")
    print(f"{BOLD}│{'PODSUMOWANIE TESTÓW'.center(summary_width)}│{RESET}")
    print(f"{BOLD}├{'─' * summary_width}┤{RESET}")
    print(f"{BOLD}│{f' Łącznie testów: {total_passed + total_failed}'.ljust(summary_width - 1)} │{RESET}")
    print(f"{BOLD}│{f' {GREEN}Zdane: {total_passed}{RESET}'.ljust(summary_width + len(GREEN) + len(RESET) - 1)} │{RESET}")
    print(f"{BOLD}│{f' {RED}Niezdane: {total_failed}{RESET}'.ljust(summary_width + len(RED) + len(RESET) - 1)} │{RESET}")
    print(f"{BOLD}╰{'─' * summary_width}╯{RESET}")

    if total_failed > 0:
        print(f"{RED}{BOLD}UWAGA: Wykryto problemy w {total_failed} przypadkach testowych!{RESET}")