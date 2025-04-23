import numpy as np
from typing import Tuple


def calculate_probability_distribution(num_elements: int) -> np.ndarray:
    """Вычисляет линейно убывающее распределение вероятностей.

    Вероятности рассчитываются по формуле: P(i) = 2*(N-i)/(N*(N+1)),
    где i - индекс элемента (0 <= i < N).

    Args:
        num_elements: Количество элементов в распределении.

    Returns:
        Массив numpy с нормализованными вероятностями.
    """
    normalization_factor = 2 / (num_elements * (num_elements + 1))
    indices = np.arange(num_elements)
    return (num_elements - indices) * normalization_factor


def compute_expected_comparisons(probabilities: np.ndarray) -> float:
    """Вычисляет математическое ожидание количества сравнений при поиске.

    Args:
        probabilities: Массив вероятностей элементов.

    Returns:
        Ожидаемое среднее количество сравнений.
    """
    # Создаем матричные версии вероятностей для векторных операций
    prob_col = probabilities[:, np.newaxis]  # Вертикальный вектор
    prob_row = probabilities[np.newaxis, :]  # Горизонтальный вектор

    # Вычисляем знаменатели, избегая деления на ноль
    sum_probs = prob_col + prob_row
    with np.errstate(divide='ignore', invalid='ignore'):
        comparison_terms = np.where(
            sum_probs != 0,
            (prob_col * prob_row) / sum_probs,
            0.0
        )

    return 0.5 + np.sum(comparison_terms)


def run_probability_experiment(num_elements: int) -> Tuple[np.ndarray, float]:
    """Запускает полный эксперимент с вычислением вероятностей и сравнений.

    Args:
        num_elements: Количество элементов в распределении.

    Returns:
        Кортеж (вероятности, ожидаемое_количество_сравнений)
    """
    probabilities = calculate_probability_distribution(num_elements)
    expected_comparisons = compute_expected_comparisons(probabilities)
    return probabilities, expected_comparisons


def main() -> None:
    """Основная функция для демонстрации работы алгоритма."""
    NUM_ELEMENTS = 1000

    probabilities, result = run_probability_experiment(NUM_ELEMENTS)

    print("Первые 100 вероятностей:", probabilities[:100])
    print("Ожидаемое количество сравнений:", f"{result:.6f}")


if __name__ == "__main__":
    main()