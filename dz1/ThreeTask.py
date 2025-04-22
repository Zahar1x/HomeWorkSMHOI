import numpy as np
import random
import math
import os

FILENAME = "keys_array.txt"


# Генерация массива целочисленных ключей
def generate_keys(size):
    keys = random.sample(range(1, size + 1), size)  # Генерируем уникальные числа в диапазоне от 1 до size
    return keys


# Сохранение исходного массива в файл
def save_keys_to_file(keys, filename=FILENAME):
    with open(filename, 'w', encoding='utf-8') as f:
        for key in keys:
            f.write(f"{key}\n")


# Чтение массива из файла
def read_keys_from_file(filename=FILENAME):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден. Генерация нового массива и сохранение в файл.")
        keys = generate_keys(500)  # Если файл не существует, генерируем новый массив
        save_keys_to_file(keys, filename)  # Сохраняем в файл
        return keys

    with open(filename, 'r', encoding='utf-8') as f:
        keys = [int(line.strip()) for line in f.readlines()]
    return keys


# Геометрическое распределение
def geometric_distribution(size, p=0.5):
    dist = [p * (1 - p) ** i for i in range(size)]
    dist = np.array(dist)
    dist /= dist.sum()  # Нормируем, чтобы сумма вероятностей была 1
    return dist


# Биномиальное распределение
def binomial_distribution(size, n=10, p=0.5):
    dist = []
    for k in range(size):
        if k <= n:  # Проверка, чтобы индекс не выходил за пределы
            dist.append(math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)))
        else:
            dist.append(0)

    dist = np.array(dist)
    dist /= dist.sum()  # Нормируем
    return dist


# Клиновидное распределение
def triangular_distribution(size):
    dist = [2 * i / (size * (size - 1)) if i < size / 2 else 2 * (size - i) / (size * (size - 1)) for i in range(size)]
    dist = np.array(dist)
    dist /= dist.sum()  # Нормируем
    return dist


# Переупорядочивание массива в соответствии с распределением
def reorder_keys(keys, dist):
    dist_indices = list(range(len(keys)))
    sorted_indices = sorted(dist_indices, key=lambda x: dist[x], reverse=True)
    return [keys[i] for i in sorted_indices]


# Линейный поиск
def linear_search(keys, query):
    for i, key in enumerate(keys):
        if key == query:
            return i
    return -1


# подсчет операций сравнения при поиске ключей
def search_experiment(keys, dist, n_queries=100000):
    comparison_count = 0
    reordered_keys = reorder_keys(keys, dist)

    for _ in range(n_queries):
        query = random.choice(keys)
        for i, key in enumerate(reordered_keys):
            comparison_count += 1
            if key == query:
                break

    avg_comparisons = comparison_count / n_queries
    return avg_comparisons


# Теоретическое среднее для каждого распределения
def theoretical_mean(dist_type, size, p=0.5, n=10):
    if dist_type == 'geometric':
        return 1 / p
    elif dist_type == 'binomial':
        return n * p
    elif dist_type == 'triangular':
        return size / 2
    else:
        return None


# Среднее количество сравнений для упорядоченного массива
def ordered_search_experiment(keys, dist, n_queries=100000):
    comparison_count = 0
    ordered_keys = sorted(keys)  # Упорядочиваем массив

    for _ in range(n_queries):
        query = random.choice(keys)
        for i, key in enumerate(ordered_keys):
            comparison_count += 1
            if key == query:
                break

    avg_comparisons = comparison_count / n_queries
    return avg_comparisons


# Основная часть программы для проведения эксперимента
def main():
    # Сначала проверим наличие файла с исходными ключами
    keys = read_keys_from_file()

    # Генерируем распределения
    geometric_dist = geometric_distribution(len(keys))
    binomial_dist = binomial_distribution(len(keys))
    triangular_dist = triangular_distribution(len(keys))

    print("Запуск эксперимента для геометрического распределения...")
    geometric_comparisons_unsorted = search_experiment(keys, geometric_dist)
    geometric_comparisons_sorted = ordered_search_experiment(keys, geometric_dist)
    geometric_theoretical_mean = theoretical_mean('geometric', len(keys), p=0.5)

    print("Запуск эксперимента для биномиального распределения...")
    binomial_comparisons_unsorted = search_experiment(keys, binomial_dist)
    binomial_comparisons_sorted = ordered_search_experiment(keys, binomial_dist)
    binomial_theoretical_mean = theoretical_mean('binomial', len(keys), p=0.5, n=10)

    print("Запуск эксперимента для клиновидного распределения...")
    triangular_comparisons_unsorted = search_experiment(keys, triangular_dist)
    triangular_comparisons_sorted = ordered_search_experiment(keys, triangular_dist)
    triangular_theoretical_mean = theoretical_mean('triangular', len(keys))

    print(f"Геометрическое распределение:")
    print(f"  Теоретическое среднее: {geometric_theoretical_mean}")
    print(f"  Среднее количество операций для неупорядоченного массива: {geometric_comparisons_unsorted}")
    print(f"  Среднее количество операций для упорядоченного массива: {geometric_comparisons_sorted}")

    print(f"\nБиномиальное распределение:")
    print(f"  Теоретическое среднее: {binomial_theoretical_mean}")
    print(f"  Среднее количество операций для неупорядоченного массива: {binomial_comparisons_unsorted}")
    print(f"  Среднее количество операций для упорядоченного массива: {binomial_comparisons_sorted}")

    print(f"\nКлиновидное распределение:")
    print(f"  Теоретическое среднее: {triangular_theoretical_mean}")
    print(f"  Среднее количество операций для неупорядоченного массива: {triangular_comparisons_unsorted}")
    print(f"  Среднее количество операций для упорядоченного массива: {triangular_comparisons_sorted}")


if __name__ == "__main__":
    main()




