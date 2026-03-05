from dataclasses import dataclass, asdict
from typing import Dict
from datetime import datetime
import json

DATA_FILE = "simulation_history.json"


@dataclass
class SimulationInput:
    employees: int
    avg_salary: float
    transport_cost_per_employee: float
    meal_cost_per_employee: float
    overhead_percent: float  # ex: 15 = 15%


def calculate_cost(s: SimulationInput) -> Dict[str, float]:
    payroll = s.employees * s.avg_salary
    transport = s.employees * s.transport_cost_per_employee
    meals = s.employees * s.meal_cost_per_employee

    direct_cost = payroll + transport + meals
    overhead = direct_cost * (s.overhead_percent / 100.0)
    total_monthly = direct_cost + overhead

    return {
        "payroll": round(payroll, 2),
        "transport": round(transport, 2),
        "meals": round(meals, 2),
        "direct_cost": round(direct_cost, 2),
        "overhead": round(overhead, 2),
        "total_monthly": round(total_monthly, 2),
        "total_yearly": round(total_monthly * 12, 2),
        "cost_per_employee": round(total_monthly / s.employees, 2) if s.employees else 0.0,
    }


def load_history():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(record: dict):
    history = load_history()
    history.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def prompt_float(label: str) -> float:
    while True:
        try:
            value = float(input(label).replace(",", "."))
            if value < 0:
                print("Valor não pode ser negativo.")
                continue
            return value
        except ValueError:
            print("Entrada inválida. Digite um número.")


def prompt_int(label: str) -> int:
    while True:
        try:
            value = int(input(label))
            if value <= 0:
                print("Digite um número maior que zero.")
                continue
            return value
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def main():
    print("\n=== Operational Cost Simulator / Simulador de Custo Operacional ===\n")

    employees = prompt_int("Employees / Funcionários: ")
    avg_salary = prompt_float("Average salary (monthly) / Salário médio (mensal): R$ ")
    transport = prompt_float("Transport per employee / Transporte por funcionário: R$ ")
    meals = prompt_float("Meals per employee / Alimentação por funcionário: R$ ")
    overhead = prompt_float("Overhead (%) / Custos indiretos (%): ")

    sim_input = SimulationInput(
        employees=employees,
        avg_salary=avg_salary,
        transport_cost_per_employee=transport,
        meal_cost_per_employee=meals,
        overhead_percent=overhead,
    )

    result = calculate_cost(sim_input)

    print("\n--- Results / Resultados ---")
    print(f"Payroll / Folha: R$ {result['payroll']:.2f}")
    print(f"Transport / Transporte: R$ {result['transport']:.2f}")
    print(f"Meals / Alimentação: R$ {result['meals']:.2f}")
    print(f"Direct cost / Custo direto: R$ {result['direct_cost']:.2f}")
    print(f"Overhead / Indiretos: R$ {result['overhead']:.2f}")
    print(f"Total monthly / Total mensal: R$ {result['total_monthly']:.2f}")
    print(f"Total yearly / Total anual: R$ {result['total_yearly']:.2f}")
    print(f"Cost per employee / Custo por funcionário: R$ {result['cost_per_employee']:.2f}")

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "input": asdict(sim_input),
        "result": result,
    }
    save_history(record)

    print("\nSaved to simulation_history.json / Salvo em simulation_history.json ✅\n")


if __name__ == "__main__":
    main()
