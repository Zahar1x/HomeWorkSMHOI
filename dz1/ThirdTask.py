import math

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import bisect
import json


class KeyExperiment:
    def __init__(self, size=300):
        self.size = size
        self.keys = np.random.permutation(10 * size)[:size]  # Уникальные ключи
        self.distributions = {
            'geometric': self._geometric_dist,
            'binomial': self._binomial_dist,
            'wedge': self._wedge_dist
        }

    def _geometric_dist(self):
        """Геометрическое распределение"""
        p = 0.3
        probs = np.array([p * (1 - p) ** i for i in range(self.size)])
        return probs / probs.sum()

    def _binomial_dist(self):
        """Биномиальное распределение"""
        n = self.size - 1
        p = 0.4
        probs = np.array([math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(self.size)])
        return probs / probs.sum()

    def _wedge_dist(self):
        """Клиновидное распределение"""
        c = 2 / (self.size * (self.size + 1))  # Нормировочная константа
        probs = np.array([(self.size - i) * c for i in range(self.size)])
        return probs / probs.sum()

    def reorder_keys(self, distribution):
        """Переупорядочивает ключи согласно распределению"""
        if distribution not in self.distributions:
            raise ValueError("Неизвестное распределение")

        probs = self.distributions[distribution]()
        sorted_idx = np.argsort(-probs)  # Сортируем по убыванию вероятности
        return self.keys[sorted_idx]

    def linear_search(self, keys, queries):
        """Линейный поиск с подсчетом сравнений"""
        comparisons = 0
        for query in queries:
            for i, key in enumerate(keys):
                comparisons += 1
                if key == query:
                    break
        return comparisons

    def run_experiment(self, num_queries=100000):
        """Проводит полный эксперимент"""
        results = {}

        for dist_name in self.distributions:
            # Переупорядочиваем ключи
            ordered_keys = self.reorder_keys(dist_name)

            # Генерируем запросы согласно распределению
            probs = self.distributions[dist_name]()
            queries = np.random.choice(ordered_keys, size=num_queries, p=probs)

            # 1. Поиск в упорядоченном массиве
            ordered_comparisons = self.linear_search(ordered_keys, queries)

            # 2. Поиск в случайном порядке (перемешиваем)
            shuffled_keys = np.random.permutation(ordered_keys)
            shuffled_comparisons = self.linear_search(shuffled_keys, queries)

            # Сохраняем результаты
            results[dist_name] = {
                'ordered_avg': ordered_comparisons / num_queries,
                'random_avg': shuffled_comparisons / num_queries,
                'theoretical': self.calculate_theoretical_avg(probs)
            }

            # Сохраняем данные для визуализации
            # self.save_distribution_plot(dist_name, ordered_keys, probs)

        return results

    def calculate_theoretical_avg(self, probs):
        """Вычисляет теоретическое среднее число сравнений"""
        return sum((i + 1) * p for i, p in enumerate(probs))

    def save_distribution_plot(self, dist_name, keys, probs):
        """Сохраняет график распределения"""
        plt.figure(figsize=(10, 5))
        plt.bar(range(len(keys)), probs[np.argsort(keys)])
        plt.title(f"Распределение вероятностей ({dist_name})")
        plt.xlabel("Ключ")
        plt.ylabel("Вероятность")
        plt.savefig(f"{dist_name}_distribution.png")
        plt.close()

    def save_results(self, results, filename="experiment_results.json"):
        """Сохраняет результаты эксперимента в файл"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)


# Запуск эксперимента
if __name__ == "__main__":
    experiment = KeyExperiment(size=300)
    results = experiment.run_experiment(num_queries=100000)

    # Вывод результатов
    print("\nРезультаты эксперимента (среднее число сравнений):")
    for dist, data in results.items():
        print(f"\nРаспределение: {dist}")
        print(f"Упорядоченный массив: {data['ordered_avg']:.2f}")
        print(f"Случайный порядок: {data['random_avg']:.2f}")
        print(f"Теоретическое значение: {data['theoretical']:.2f}")

    # Сохранение результатов
    experiment.save_results(results)
    print("\nРезультаты сохранены в experiment_results.json")