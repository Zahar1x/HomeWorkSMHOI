import numpy as np


class Condition:
    def __init__(self, T, P):
        self.T = T  # Время проверки
        self.P = P  # Вероятность выполнения


# Функция для вычисления среднего времени выполнения проверок
def calculate_expected_time(conditions):
    time = 0.0
    product = 1.0
    for cond in conditions:
        time += product * cond.T  # добавляем время на условие
        product *= cond.P  # добавляем вклад условия для следующих проверок
    return time


# Тестирование
def test(N, num_conditions):
    total_unsorted_time = 0.0
    total_sorted_time = 0.0

    for _ in range(N):
        # Генерация случайных условий
        conditions = [
            Condition(T=np.random.uniform(1, 11), P=np.random.uniform(0.05, 0.95))
            for _ in range(num_conditions)
        ]

        # Вычисление времени для неупорядоченного порядка
        unsorted_time = calculate_expected_time(conditions)
        total_unsorted_time += unsorted_time

        # Сортировка условий по возрастанию отношения T/P
        conditions.sort(key=lambda x: x.T / x.P)

        # Вычисление времени для оптимального порядка
        sorted_time = calculate_expected_time(conditions)
        total_sorted_time += sorted_time

    avg_unsorted_time = total_unsorted_time / N
    avg_sorted_time = total_sorted_time / N

    return avg_unsorted_time, avg_sorted_time


# Пример использования с вводом пользователя
if __name__ == "__main__":
    N = 1000  # Количество тестов
    num_conditions = int(input("Введите количество условий: "))  # Ввод от пользователя
    avg_unsorted_time, avg_sorted_time = test(N, num_conditions)

    print(f"Среднее время для неупорядоченных условий: {avg_unsorted_time:.4f}")
    print(f"Среднее время для упорядоченных условий: {avg_sorted_time:.4f}")

    # Выводим, во сколько раз быстрее оптимальный порядок
    if avg_unsorted_time > 0:
        speedup = avg_unsorted_time / avg_sorted_time
        print(f"Оптимальный порядок быстрее в {speedup:.2f} раз.")
    else:
        print("Среднее время для неупорядоченных условий равно 0, невозможно рассчитать ускорение.")

