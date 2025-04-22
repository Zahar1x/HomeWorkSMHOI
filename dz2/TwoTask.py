import numpy as np
import random


N = 10_000  # Количество записей
SEARCH_COUNT = 1000  # Кол-во поисков для оценки стоимости


def generate_tape(distribution, n):
    if distribution == "geometric":
        return np.random.geometric(p=0.05, size=n).tolist()
    elif distribution == "binomial":
        return np.random.binomial(n=100, p=0.5, size=n).tolist()
    elif distribution == "uniform":
        return np.random.randint(0, 1000, size=n).tolist()
    else:
        raise ValueError("Неизвестный метод")


# Линейный поиск (для неупорядоченной ленты)
def linear_search(tape, target):
    cost = 0
    for item in tape:
        cost += 1
        if item == target:
            break
    return cost


# Бинарный поиск (для упорядоченной ленты)
def binary_search(tape, target):
    low = 0
    high = len(tape) - 1
    cost = 0
    while low <= high:
        mid = (low + high) // 2
        cost += 1
        if tape[mid] == target:
            return cost
        elif tape[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return cost  # Возвращаем стоимость, даже если элемент не найден


# Многократный поиск
def run_search_tests(tape, ordered=False):
    if ordered:
        tape.sort()

    costs = []
    for _ in range(SEARCH_COUNT):
        target = random.choice(tape)
        if ordered:
            cost = binary_search(tape, target)
        else:
            cost = linear_search(tape, target)
        costs.append(cost)

    avg_cost = sum(costs) / len(costs)
    return avg_cost


# Главная функция
def main():
    distributions = ["geometric", "binomial", "uniform"]
    for dist in distributions:
        print(f"\n--- Распределение: {dist} ---")
        tape = generate_tape(dist, N)

        avg_cost_unsorted = run_search_tests(tape.copy(), ordered=False)
        avg_cost_sorted = run_search_tests(tape.copy(), ordered=True)

        print(f"Средняя стоимость (неупорядоченная): {avg_cost_unsorted:.2f}")
        print(f"Средняя стоимость (упорядоченная):   {avg_cost_sorted:.2f}")

if __name__ == "__main__":
    main()
