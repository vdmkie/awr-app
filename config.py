import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', "YOUR_BOT_TOKEN_HERE")  # Замените на ваш токен бота
SUPER_GROUP_ID = os.getenv('SUPER_GROUP_ID', "YOUR_SUPER_GROUP_ID")  # ID супергруппы для отчетов

# Авторизованные номера телефонов (без +)
AUTHORIZED_PHONES = [
    "79161234567",  # Супер-админ
    "79161234568",  # Админ 1
    "79161234569",  # Админ 2
    "79161234570",  # Бригада 1
    "79161234571",  # Бригада 2
    "79161234572",  # Бригада 3
    "79161234573",  # Бригада 4
    "79161234574",  # Бригада 5
    "79161234575",  # Бригада 6
    "79161234576",  # Бригада 7
    "79161234577",  # Бригада 8
    "79161234578",  # Бригада 9
    "79161234579",  # Бригада 10
    "79161234580",  # Кладовщик
]

# Пользователи системы (логин: {пароль, роль, имя})
# ВАЖНО: Пароли хешированы для безопасности
USERS = {
    "superadmin": {
        "password": generate_password_hash("admin123"),
        "role": "super_admin",
        "name": "Супер Администратор",
        "phone": "79161234567"
    },
    "admin1": {
        "password": generate_password_hash("admin1pass"),
        "role": "admin",
        "name": "Администратор 1",
        "phone": "79161234568"
    },
    "admin2": {
        "password": generate_password_hash("admin2pass"),
        "role": "admin",
        "name": "Администратор 2",
        "phone": "79161234569"
    },
    "brigade1": {
        "password": generate_password_hash("brig1pass"),
        "role": "brigade",
        "name": "Бригада 1",
        "phone": "79161234570"
    },
    "brigade2": {
        "password": generate_password_hash("brig2pass"),
        "role": "brigade",
        "name": "Бригада 2",
        "phone": "79161234571"
    },
    "brigade3": {
        "password": generate_password_hash("brig3pass"),
        "role": "brigade",
        "name": "Бригада 3",
        "phone": "79161234572"
    },
    "brigade4": {
        "password": generate_password_hash("brig4pass"),
        "role": "brigade",
        "name": "Бригада 4",
        "phone": "79161234573"
    },
    "brigade5": {
        "password": generate_password_hash("brig5pass"),
        "role": "brigade",
        "name": "Бригада 5",
        "phone": "79161234574"
    },
    "brigade6": {
        "password": generate_password_hash("brig6pass"),
        "role": "brigade",
        "name": "Бригада 6",
        "phone": "79161234575"
    },
    "brigade7": {
        "password": generate_password_hash("brig7pass"),
        "role": "brigade",
        "name": "Бригада 7",
        "phone": "79161234576"
    },
    "brigade8": {
        "password": generate_password_hash("brig8pass"),
        "role": "brigade",
        "name": "Бригада 8",
        "phone": "79161234577"
    },
    "brigade9": {
        "password": generate_password_hash("brig9pass"),
        "role": "brigade",
        "name": "Бригада 9",
        "phone": "79161234578"
    },
    "brigade10": {
        "password": generate_password_hash("brig10pass"),
        "role": "brigade",
        "name": "Бригада 10",
        "phone": "79161234579"
    },
    "warehouse": {
        "password": generate_password_hash("warehouse123"),
        "role": "warehouse",
        "name": "Кладовщик",
        "phone": "79161234580"
    }
}

# Материалы и их единицы измерения
MATERIALS = {
    "Кабель ВОК 4 100": "м",
    "БО/16 100": "шт",
    "Шпаклёвка 100": "кг"
}

# Виды работ
WORK_TYPES = [
    "воздушка",
    "перемычка",
    "растянуть дом",
    "дом под ключ",
    "бурение",
    "сварки"
]

# Статусы задач
TASK_STATUSES = [
    "Новая задача",
    "В работе",
    "Выполнено",
    "Отложено",
    "Проблемный дом"
]

# Статусы бригад
BRIGADE_STATUSES = [
    "в работе",
    "на больничном",
    "в командировке",
    "в отпуске",
    "увольняются"
]

# Секретный ключ для Flask сессий
SECRET_KEY = "awr_secret_key_2025"

# Пути к данным
DATA_DIR = "data"
UPLOADS_DIR = "uploads"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"

# Создание директорий если их нет
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(f"{UPLOADS_DIR}/photos", exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(f"{STATIC_DIR}/css", exist_ok=True)
os.makedirs(f"{STATIC_DIR}/js", exist_ok=True)
os.makedirs(f"{STATIC_DIR}/images", exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
