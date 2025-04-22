import os

FILENAME = "large_data.txt"
TEMP_FILENAME = "temp_file.txt"


def search_and_remove_records(filename, query, field):
    found = []
    remaining = []

    with open(filename, 'r', encoding='utf-8') as f:
        header = f.readline().strip()  # Читаем заголовок
        # Начинаем обработку записей с оставшимися строками
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(';')
            if len(parts) != 5:
                remaining.append(line)
                continue

            # Поиск по полям
            if field == 'id' and query.lower() in parts[0].lower():
                found.append(line)
            elif field == 'tags' and query in parts[4]:
                found.append(line)
            elif field == 'status' and query.lower() in parts[1].lower():
                found.append(line)
            else:
                remaining.append(line)

    return found, remaining, header


def append_to_temp_file(temp_filename, found, remaining, header):
    with open(temp_filename, 'w', encoding='utf-8') as f:
        # Записываем заголовок один раз
        f.write(header + '\n')
        # Сначала записываем найденные записи
        for record in found:
            f.write(record + '\n')

        # Затем записываем оставшиеся записи
        for record in remaining:
            f.write(record + '\n')


def replace_file_with_temp():
    if os.path.exists(TEMP_FILENAME):
        os.replace(TEMP_FILENAME, FILENAME)
        print("Файл обновлён!")


def main():
    if not os.path.exists(FILENAME):
        print(f"Файл {FILENAME} не найден.")
        return

    while True:
        print("\n=== Система поиска в текстовом файле ===")
        print("1. Поиск по ID")
        print("2. Поиск по тегу")
        print("3. Поиск по статусу")
        print("4. Добавить запись")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ")

        if choice == '5':
            break

        query = input("Введите запрос: ").strip()
        field_map = {'1': 'id', '2': 'tags', '3': 'status'}
        field = field_map.get(choice)

        if not field:
            print("Неверный выбор.")
            continue

        found, remaining, header = search_and_remove_records(FILENAME, query, field)

        if found:
            print(f"\nНайдено записей: {len(found)}")
            for r in found[:10]:  # показываем первые 10 найденных
                print(r)

            # Перезаписываем файл: сначала найденные записи, затем оставшиеся
            append_to_temp_file(TEMP_FILENAME, found, remaining, header)
            replace_file_with_temp()
        else:
            print("Совпадений не найдено.")


if __name__ == "__main__":
    main()

