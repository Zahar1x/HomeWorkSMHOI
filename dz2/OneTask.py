import random


# Генерация случайного массива уникальных чисел
def generate_random_array(size):
    return random.sample(range(1, size * 10), size)  # Массив из уникальных чисел


# Запись массива в файл
def write_array_to_file(filename, arr):
    with open(filename, 'w') as f:
        for num in arr:
            f.write(f"{num}\n")


# Чтение массива из файла
def read_array_from_file(filename):
    with open(filename, 'r') as f:
        arr = [int(line.strip()) for line in f.readlines()]
    return arr


# Линейный поиск в массиве
def linear_search(arr, target):
    comparisons = 0
    for element in arr:
        comparisons += 1
        if element == target:
            break
    return comparisons


# Среднее количество сравнений для массива
def average_comparisons(arr, n_queries=100000):
    total_comparisons = 0
    for _ in range(n_queries):
        target = random.choice(arr)  # случайный элемент для поиска
        total_comparisons += linear_search(arr, target)
    return total_comparisons / n_queries


# Основная функция для проведения эксперимента
def experiment(filename):
    # Чтение массива из файла
    arr = read_array_from_file(filename)

    # Наилучшее расположение (по убыванию)
    best_arr = sorted(arr, reverse=True)
    # Наихудшее расположение (по возрастанию)
    worst_arr = sorted(arr)

    # Подсчитаем среднее количество сравнений для наилучшего и наихудшего расположения
    best_avg_comparisons = average_comparisons(best_arr)
    worst_avg_comparisons = average_comparisons(worst_arr)

    # Выводим результаты
    print(f"Среднее количество сравнений для наилучшего расположения: {best_avg_comparisons:.2f}")
    print(f"Среднее количество сравнений для наихудшего расположения: {worst_avg_comparisons:.2f}")


# Основная функция
def main():
    size = 500 # Размер массива
    filename = 'random_array.txt'  # Имя файла для записи массива

    # Генерация случайного массива
    arr = generate_random_array(size)

    # Запись массива в файл
    write_array_to_file(filename, arr)

    # Проведение эксперимента
    experiment(filename)


if __name__ == "__main__":
    main()
