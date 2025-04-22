import numpy as np


def p3(N):
    i = np.arange(N, dtype=float)
    probabilities = 1 / np.power(2, i)
    return probabilities


def calc_cn(prob):
    prob = np.array(prob)
    Pi = prob[:, np.newaxis]  # превращаем в столбец
    Pj = prob[np.newaxis, :]  # превращаем в строку

    denominator = Pi + Pj
    # избегаем деления на ноль
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = np.where(denominator != 0, (Pi * Pj) / denominator, 0.0)

    result = 0.5 + np.sum(terms)
    return result


# Главная функция
def main():
    N = 1000
    probabilities = p3(N)
    result = calc_cn(probabilities)

    print("Вероятности:", probabilities)
    print("Результат вычисления:", result)


if __name__ == "__main__":
    main()