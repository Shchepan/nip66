import sys
from src.manager import Manager
from src.models import Parameters

def print_section_header(title: str):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")

def print_subsection_header(title: str):
    print(f"\n  {title}")
    print(f"  {'-' * 40}")

def format_currency(amount: float) -> str:
    return f"{amount:,.2f} PLN"

def display_settlement_report(manager, apartment_key: str, year: int, month: int):
    settlement = manager.get_settlement(apartment_key, year, month)
    
    if settlement is None:
        print(f"\n Błąd: Nie znaleziono danych rozliczeniowych dla '{apartment_key}' w okresie {month}/{year}.")
        return

    print_section_header(f"RAPORT ROZLICZENIOWY: {apartment_key}")
    print(f"Okres: {month}/{year}")
    print(f"Całkowite koszty mieszkania: {format_currency(settlement.total_due_pln)}")

    tenant_settlements = manager.create_tenants_settlements(settlement)
    
    if not tenant_settlements:
        print("\n⚠️ Brak lokatorów przypisanych do tego mieszkania w podanym okresie.")
    else:
        print_subsection_header("Podział kosztów na lokatorów")
        for ts in tenant_settlements:
            print(f"👤 {ts.tenant:<25} {format_currency(ts.total_due_pln):>15}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("\nSposób użycia: python main.py <klucz_mieszkania> <rok> <miesiąc>")
        sys.exit(1)

    apartment_key = sys.argv[1]
    
    try:
        year = int(sys.argv[2])
        month = int(sys.argv[3])
    except ValueError:
        print("\n Błąd: Rok i miesiąc muszą być liczbami całkowitymi.")
        sys.exit(1)

    parameters = Parameters()
    manager = Manager(parameters)

    display_settlement_report(manager, apartment_key, year, month)
    
    print(f"\n{'=' * 70}\n")
