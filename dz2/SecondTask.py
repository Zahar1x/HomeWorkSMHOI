import random
from typing import List, Dict, Callable
import numpy as np

NUM_RECORDS = 10_000  # Количество записей в ленте
SEARCH_ITERATIONS = 1_000  # Количество тестов поиска для оценки


def generate_tape(distribution: str, size: int) -> List[int]:
    """Генерирует ленту данных согласно заданному распределению.

    Аргументы:
        distribution: тип распределения ("geometric", "binomial", "uniform")
        size: количество элементов в ленте

    Возвращает:
        Список сгенерированных значений

    Исключения:
        ValueError: если передано неизвестное распределение
    """
    generators: Dict[str, Callable] = {
        "geometric": lambda: np.random.geometric(p=0.05, size=size),
        "binomial": lambda: np.random.binomial(n=100, p=0.5, size=size),
        "uniform": lambda: np.random.randint(0, 1000, size=size)
    }

    if distribution not in generators:
        raise ValueError(f"Неизвестное распределение: {distribution}")

    return generators[distribution]().tolist()


def linear_search(tape: List[int], target: int) -> int:
    """Выполняет линейный поиск и возвращает количество сравнений."""
    comparisons = 0
    for item in tape:
        comparisons += 1
        if item == target:
            break
    return comparisons


def binary_search(sorted_tape: List[int], target: int) -> int:
    """Выполняет бинарный поиск в отсортированном массиве и возвращает количество сравнений."""
    left, right = 0, len(sorted_tape) - 1
    comparisons = 0

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        if sorted_tape[mid] == target:
            return comparisons
        elif sorted_tape[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return comparisons


def evaluate_search_performance(tape: List[int], is_ordered: bool = False) -> float:
    """Оценивает среднюю стоимость поиска для заданной ленты.

    Аргументы:
        tape: лента данных для поиска
        is_ordered: флаг, указывающий на отсортированность ленты

    Возвращает:
        Среднее количество сравнений при поиске
    """
    search_function = binary_search if is_ordered else linear_search
    total_comparisons = 0

    for _ in range(SEARCH_ITERATIONS):
        target = random.choice(tape)
        total_comparisons += search_function(tape, target)

    return total_comparisons / SEARCH_ITERATIONS


def run_experiments() -> None:
    """Запускает серию экспериментов для разных распределений данных."""
    distributions = ("geometric", "binomial", "uniform")

    for distribution in distributions:
        print(f"\n=== Распределение: {distribution} ===")

        data_tape = generate_tape(distribution, NUM_RECORDS)

        # Оценка для неупорядоченных данных
        unordered_cost = evaluate_search_performance(data_tape.copy())

        # Оценка для упорядоченных данных
        ordered_tape = sorted(data_tape.copy())
        ordered_cost = evaluate_search_performance(ordered_tape, is_ordered=True)

        print(f"Средняя стоимость поиска:")
        print(f"  Неупорядоченная лента: {unordered_cost:.2f}")
        print(f"  Упорядоченная лента:   {ordered_cost:.2f}")


if __name__ == "__main__":
    run_experiments()