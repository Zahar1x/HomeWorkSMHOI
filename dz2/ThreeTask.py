import numpy as np


def generate_probabilities(num_elements: int) -> np.ndarray:
    """Генерирует массив вероятностей по формуле 1/2^(i-1).

    Args:
        num_elements: Количество элементов в массиве вероятностей.

    Returns:
        Массив numpy с рассчитанными вероятностями.
    """
    indices = np.arange(num_elements, dtype=np.float64)
    return 1 / np.power(2, indices - 1)


def calculate_expected_comparisons(probabilities: np.ndarray) -> float:
    """Вычисляет математическое ожидание количества сравнений.

    Args:
        probabilities: Массив вероятностей.

    Returns:
        Ожидаемое количество сравнений (значение Cn).
    """
    # Преобразуем в столбцовую и строчную матрицы для векторных операций
    prob_col = probabilities[:, np.newaxis]
    prob_row = probabilities[np.newaxis, :]

    # Вычисляем знаменатель, избегая деления на ноль
    denominator = prob_col + prob_row
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = np.where(denominator != 0,
                         (prob_col * prob_row) / denominator,
                         0.0)

    return 0.5 + np.sum(terms)


def main() -> None:
    """Основная функция для демонстрации работы алгоритма."""
    NUM_ELEMENTS = 1000

    probabilities = generate_probabilities(NUM_ELEMENTS)
    expected_comparisons = calculate_expected_comparisons(probabilities)

    print("Первые 100 вероятностей:", probabilities[:100])
    print("Ожидаемое количество сравнений:", expected_comparisons)


if __name__ == "__main__":
    main()