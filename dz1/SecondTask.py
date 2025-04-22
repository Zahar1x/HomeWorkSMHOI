import os
from datetime import datetime
from collections import defaultdict


class SelfOrganizingTextFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.index = {}  # {record_id: file_position}
        self.tag_index = defaultdict(list)  # {tag: [positions]}
        self.status_index = defaultdict(list)  # {status: [positions]}
        self._build_indexes()

    def _build_indexes(self):
        """Построение индексов при инициализации"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл {self.file_path} не найден!")

        with open(self.file_path, "r+") as f:
            pos = 0
            while True:
                line_start = pos
                line = f.readline()
                if not line:
                    break

                parts = line.strip().split(";")
                if len(parts) != 5:
                    continue

                record_id = parts[0]
                self.index[record_id] = line_start

                # Индексируем теги
                tags = parts[4].split(",")
                for tag in tags:
                    self.tag_index[tag].append(line_start)

                # Индексируем статусы
                status = parts[1]
                self.status_index[status].append(line_start)

                pos = f.tell()

    def _read_record(self, pos: int) -> str:
        """Читает запись по позиции в файле"""
        with open(self.file_path, "r") as f:
            f.seek(pos)
            return f.readline().strip()

    def _move_to_front(self, pos: int):
        """Перемещает запись в начало файла"""
        # Читаем запись для перемещения
        with open(self.file_path, "r") as f:
            f.seek(pos)
            record = f.readline()
            record_length = len(record.encode('utf-8'))

        # Читаем весь файл
        with open(self.file_path, "r") as f:
            content = f.readlines()

        # Находим индекс записи
        with open(self.file_path, "r") as f:
            f.seek(0)
            current_pos = 0
            record_index = 0
            while current_pos < pos:
                line = f.readline()
                current_pos += len(line.encode('utf-8'))
                record_index += 1

        # Перемещаем запись
        moved_record = content.pop(record_index)
        content.insert(0, moved_record)

        # Перезаписываем файл
        with open(self.file_path, "w") as f:
            f.writelines(content)

        # Обновляем индексы
        self._update_indexes(pos, record_length, 0)

    def _update_indexes(self, old_pos: int, record_length: int, new_pos: int):
        """Обновляет индексы после перемещения записи"""
        # Обновляем главный индекс
        for rid, pos in self.index.items():
            if pos == old_pos:
                self.index[rid] = new_pos
            elif pos < old_pos:
                self.index[rid] = pos + record_length

        # Обновляем теги
        for tag in self.tag_index:
            self.tag_index[tag] = [
                new_pos if p == old_pos else
                (p + record_length if p < old_pos else p)
                for p in self.tag_index[tag]
            ]

        # Обновляем статусы
        for status in self.status_index:
            self.status_index[status] = [
                new_pos if p == old_pos else
                (p + record_length if p < old_pos else p)
                for p in self.status_index[status]
            ]

    def search_by_id(self, record_id: str) -> str:
        """Поиск по ID с самоорганизацией"""
        if record_id not in self.index:
            return None

        pos = self.index[record_id]
        record = self._read_record(pos)
        self._move_to_front(pos)
        return record

    def search_by_tag(self, tag: str, limit: int = 10) -> list:
        """Поиск по тегу"""
        if tag not in self.tag_index:
            return []

        records = []
        for pos in self.tag_index[tag][:limit]:
            records.append(self._read_record(pos))
            self._move_to_front(pos)
        return records

    def search_by_status(self, status: str, limit: int = 10) -> list:
        """Поиск по статусу"""
        if status not in self.status_index:
            return []

        records = []
        for pos in self.status_index[status][:limit]:
            records.append(self._read_record(pos))
            self._move_to_front(pos)
        return records

    def add_record(self, record: str):
        """Добавляет новую запись в конец файла"""
        if not record.endswith("\n"):
            record += "\n"

        with open(self.file_path, "a") as f:
            pos = f.tell()
            f.write(record)

        # Обновляем индексы
        parts = record.strip().split(";")
        if len(parts) == 5:
            record_id = parts[0]
            self.index[record_id] = pos

            tags = parts[4].split(",")
            for tag in tags:
                self.tag_index[tag].append(pos)

            status = parts[1]
            self.status_index[status].append(pos)


def main():
    FILE_PATH = "large_data.txt"

    try:
        db = SelfOrganizingTextFile(FILE_PATH)
    except FileNotFoundError:
        print(f"Файл {FILE_PATH} не найден!")
        return

    while True:
        print("\n=== Система поиска в текстовом файле ===")
        print("1. Поиск по ID")
        print("2. Поиск по тегу")
        print("3. Поиск по статусу")
        print("4. Добавить запись")
        print("5. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            record_id = input("Введите ID записи (9 цифр): ").strip()
            record = db.search_by_id(record_id)
            if record:
                print("\nНайдена запись:")
                print(record)
            else:
                print("Запись не найдена!")

        elif choice == "2":
            tag = input("Введите тег (например, tag_12): ").strip()
            records = db.search_by_tag(tag)
            if records:
                print(f"\nНайдено {len(records)} записей:")
                for r in records:
                    print(r)
            else:
                print("Записи не найдены!")

        elif choice == "3":
            status = input("Введите статус (ACTIVE/PENDING/COMPLETED/FAILED): ").strip().upper()
            records = db.search_by_status(status)
            if records:
                print(f"\nНайдено {len(records)} записей:")
                for r in records:
                    print(r)
            else:
                print("Записи не найдены!")

        elif choice == "4":
            print("\nФормат записи: ID;STATUS;TIMESTAMP;VALUE;TAGS")
            print("Пример: 000000042;ACTIVE;2023-05-15 14:30:45;1234.56;tag_12,tag_45")
            record = input("Введите новую запись: ").strip()
            db.add_record(record)
            print("Запись добавлена!")

        elif choice == "5":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()