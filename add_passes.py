import csv
import os

# Путь к CSV относительно скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
passes_file = os.path.join(BASE_DIR, "passes.csv")

# Функция для добавления нового пропуска
def add_pass(pass_id, name, role, filename):
    # Проверим, существует ли уже такой ID
    existing_ids = set()
    if os.path.exists(filename):
        with open(filename, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row["id"])

    if pass_id in existing_ids:
        print(f"⛔ Пропуск с ID {pass_id} уже существует!")
        return

    # Добавляем запись
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "name", "role"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Записываем заголовок в случае нового файла
        if not file_exists:
            writer.writeheader()

        writer.writerow({"id": pass_id, "name": name, "role": role.lower()})
        print(f"✅ Пропуск {pass_id} добавлен успешно!")

# Основной запуск
pass_id = input("Введите ID нового пропуска: ")
name = input("Введите имя владельца: ")
role = input("Введите роль (администратор, преподаватель, уборщик, студент): ")

add_pass(pass_id, name, role, passes_file)
