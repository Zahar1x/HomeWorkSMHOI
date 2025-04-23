import random
from typing import List


def generate_random_array(size: int) -> List[int]:
    """Генерирует массив случайных уникальных чисел."""
    return random.sample(range(1, size * 10), size)


def write_array_to_file(filename: str, array: List[int]) -> None:
    """Записывает массив в файл, каждое число на новой строке."""
    with open(filename, 'w') as file:
        file.write('\n'.join(map(str, array)))


def read_array_from_file(filename: str) -> List[int]:
    """Читает массив из файла, где каждое число на новой строке."""
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]


def linear_search(array: List[int], target: int) -> int:
    """Выполняет линейный поиск и возвращает количество сравнений."""
    comparisons = 0
    for element in array:
        comparisons += 1
        if element == target:
            break
    return comparisons


def calculate_average_comparisons(array: List[int], num_queries: int = 100_000) -> float:
    """Вычисляет среднее количество сравнений для заданного массива."""
    total_comparisons = 0
    for _ in range(num_queries):
        target = random.choice(array)
        total_comparisons += linear_search(array, target)
    return total_comparisons / num_queries


def run_experiment(filename: str) -> None:
    """Проводит эксперимент сравнения для лучшего и худшего случаев."""
    array = read_array_from_file(filename)

    best_case = sorted(array, reverse=True)
    worst_case = array

    best_avg = calculate_average_comparisons(best_case)
    worst_avg = calculate_average_comparisons(worst_case)

    print(f"Среднее количество сравнений для наилучшего расположения: {best_avg:.2f}")
    print(f"Среднее количество сравнений для наихудшего расположения: {worst_avg:.2f}")


def main() -> None:
    """Основная функция программы."""
    array_size = 500
    filename = 'random_array.txt'

    random_array = generate_random_array(array_size)
    write_array_to_file(filename, random_array)

    run_experiment(filename)


if __name__ == "__main__":
    main()