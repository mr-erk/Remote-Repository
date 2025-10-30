import os
import csv
import datetime

# Папка, где лежит скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Полные пути к файлам CSV (Позже будет облачная БД Постгресс)
passes_path = os.path.join(BASE_DIR, "passes.csv")
schedule_path = os.path.join(BASE_DIR, "schedule.csv")

# Функции для загрузки
def load_passes(filename):
    passes = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            passes[row["id"]] = {"name": row["name"], "role": row["role"].lower()}
    return passes

def load_schedule(filename):
    schedule = {}
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["id"]
            day = row["day"].lower()
            start = row["start"]
            end = row["end"]
            schedule.setdefault(pid, {}).setdefault(day, []).append((start, end))
    return schedule

def translate_day(day_en):
    days = {
        "monday": "понедельник", "tuesday": "вторник", "wednesday": "среда",
        "thursday": "четверг", "friday": "пятница",
        "saturday": "суббота", "sunday": "воскресенье"
    }
    return days.get(day_en, day_en)

def can_enter(pass_id, passes, schedule):
    now = datetime.datetime.now()
    weekday_en = now.strftime("%A").lower()
    weekday = translate_day(weekday_en)
    time_now = now.strftime("%H:%M")

    if pass_id not in passes:
        return False, "Неизвестный пропуск"

    person = passes[pass_id]
    role = person["role"]
    
    # Постоянный доступ
    if role in ("администратор", "преподаватель", "уборщик"):
        return True, f"{person['name']} ({role}) имеет постоянный доступ"

    # Студенты по расписанию
    if role == "студент":
        if pass_id not in schedule:
            return False, f"Для {person['name']} нет расписания"
        if weekday not in schedule[pass_id]:
            return False, f"Сегодня ({weekday}) у {person['name']} нет доступа"

        for start, end in schedule[pass_id][weekday]:
            if start <= time_now <= end:
                return True, f"{person['name']} ({role}) имеет доступ по расписанию"

        return False, f"Сейчас не время допуска для {person['name']}"

    return False, f"Неизвестная роль у {person['name']}"

# Загружаем данные с использованием абсолютного пути
passes = load_passes(passes_path)
schedule = load_schedule(schedule_path)

card = input("Введите номер пропуска: ")
allowed, reason = can_enter(card, passes, schedule)
print("✅ Доступ разрешён" if allowed else "⛔ Доступ запрещён", "-", reason)print('change after stashing.')
