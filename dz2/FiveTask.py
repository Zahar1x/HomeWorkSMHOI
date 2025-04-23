import numpy as np
from typing import List, Tuple


class Condition:
    """Класс, представляющий условие проверки с временем выполнения и вероятностью успеха."""

    def __init__(self, check_time: float, success_prob: float):
        """
        Args:
            check_time: Время выполнения проверки (T)
            success_prob: Вероятность успешного выполнения (P)
        """
        self.check_time = check_time
        self.success_prob = success_prob

    @property
    def time_prob_ratio(self) -> float:
        """Вычисляет отношение времени к вероятности (T/P) для оптимизации порядка."""
        return self.check_time / self.success_prob


def calculate_expected_time(conditions: List[Condition]) -> float:
    """
    Вычисляет ожидаемое общее время выполнения последовательности проверок.

    Args:
        conditions: Список условий проверки

    Returns:
        Ожидаемое суммарное время выполнения
    """
    total_time = 0.0
    cumulative_prob = 1.0  # Вероятность дойти до текущей проверки

    for condition in conditions:
        total_time += cumulative_prob * condition.check_time
        cumulative_prob *= condition.success_prob

    return total_time


def generate_random_conditions(num_conditions: int) -> List[Condition]:
    """
    Генерирует список случайных условий проверки.

    Args:
        num_conditions: Количество условий для генерации

    Returns:
        Список случайных условий
    """
    return [
        Condition(
            check_time=np.random.uniform(1, 11),
            success_prob=np.random.uniform(0.05, 0.95)
        )
        for _ in range(num_conditions)
    ]


def run_performance_test(
        num_tests: int,
        num_conditions: int
) -> Tuple[float, float, float]:
    """
    Проводит сравнение производительности упорядоченного и неупорядоченного выполнения проверок.

    Args:
        num_tests: Количество тестов для усреднения
        num_conditions: Количество условий в каждом тесте

    Returns:
        Кортеж из (среднее время без сортировки, среднее время с сортировкой, коэффициент ускорения)
    """
    total_unsorted_time = 0.0
    total_sorted_time = 0.0

    for _ in range(num_tests):
        conditions = generate_random_conditions(num_conditions)

        # Время без сортировки
        total_unsorted_time += calculate_expected_time(conditions)

        # Время с оптимальной сортировкой по возрастанию T/P
        sorted_conditions = sorted(conditions, key=lambda x: x.time_prob_ratio)
        total_sorted_time += calculate_expected_time(sorted_conditions)

    avg_unsorted = total_unsorted_time / num_tests
    avg_sorted = total_sorted_time / num_tests
    speedup = avg_unsorted / avg_sorted if avg_unsorted > 0 else 0.0

    return avg_unsorted, avg_sorted, speedup


def main():
    """Основная функция для взаимодействия с пользователем."""
    NUM_TESTS = 1000

    print("Оптимизация порядка выполнения проверок")
    num_conditions = int(input("Введите количество условий для тестирования: "))

    unsorted_time, sorted_time, speedup = run_performance_test(
        NUM_TESTS, num_conditions
    )

    print("\nРезультаты тестирования:")
    print(f"- Среднее время без оптимизации: {unsorted_time:.4f}")
    print(f"- Среднее время с оптимизацией: {sorted_time:.4f}")

    if speedup > 0:
        print(f"- Оптимальный порядок быстрее в {speedup:.2f} раз")
    else:
        print("- Невозможно рассчитать ускорение (нулевое время без оптимизации)")


if __name__ == "__main__":
    main()