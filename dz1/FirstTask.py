import random
from datetime import datetime, timedelta
import os


def generate_record(record_id: int) -> str:
    """Генерирует одну текстовую запись"""
    status = random.choice(["ACTIVE", "PENDING", "COMPLETED", "FAILED"])
    timestamp = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S")
    value = random.uniform(1, 10000)
    tags = ",".join(f"tag_{random.randint(1, 100)}" for _ in range(random.randint(1, 5)))

    return f"{record_id:09d};{status};{timestamp};{value:.2f};{tags}"


def generate_large_file(file_path: str, target_size_mb: int = 500):
    """Создает большой текстовый файл"""
    record_size_bytes = 120  # Средний размер одной записи
    records_needed = (target_size_mb * 1024 * 1024) // record_size_bytes

    with open(file_path, "w") as f:
        record_id = 0
        size = f.tell()
        while size < target_size_mb * 1024 * 1024:
            record = generate_record(record_id)
            f.write(record + '\n')
            size += len(record.encode('utf-8')) + 1
            record_id += 1
            if record_id % 1000 == 0:
                print(f"Сгенерировано {record_id} записей...")

    print(f"Файл {file_path} создан. Размер: {os.path.getsize(file_path) / (1024 ** 2):.2f} МБ")


# Запуск генерации
generate_large_file("large_data.txt", target_size_mb=500)