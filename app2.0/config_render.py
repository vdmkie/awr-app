"""
Обновленный config.py для развертывания на Render.com
Использует переменные окружения для безопасного хранения конфиденциальных данных
"""

import os
from werkzeug.security import generate_password_hash

# Настройки для Render.com
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
SUPER_GROUP_ID = int(os.getenv('SUPER_GROUP_ID', '0')) if os.getenv('SUPER_GROUP_ID') else None

# Настройки приложения
UPLOADS_DIR = 'uploads'
PHOTOS_DIR = os.path.join(UPLOADS_DIR, 'photos')

# Создание необходимых папок
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Типы работ
WORK_TYPES = [
    "Строительство",
    "Ремонт",
    "Электромонтаж", 
    "Сантехника",
    "Отделочные работы",
    "Кровельные работы",
    "Прочее"
]

# Статусы задач
TASK_STATUSES = [
    "В ожидании",
    "В работе", 
    "Выполнено",
    "Отменено",
    "Приостановлено"
]

# Статусы бригад
BRIGADE_STATUSES = [
    "Свободна",
    "Занята",
    "Недоступна"
]

# Пользователи с хешированными паролями
USERS = {
    'superadmin': {
        'password_hash': generate_password_hash('admin123'),
        'role': 'super_admin',
        'name': 'Суперадминистратор',
        'phone': '+7(900)000-00-01'
    },
    'admin1': {
        'password_hash': generate_password_hash('admin123'),
        'role': 'admin',
        'name': 'Администратор',
        'phone': '+7(900)000-00-02'
    },
    'brigade1': {
        'password_hash': generate_password_hash('brigade123'),
        'role': 'brigade',
        'name': 'Бригадир Иванов',
        'phone': '+7(900)000-00-03'
    },
    'warehouse1': {
        'password_hash': generate_password_hash('warehouse123'),
        'role': 'warehouse',
        'name': 'Кладовщик Петров',
        'phone': '+7(900)000-00-04'
    }
}

# Телефоны для авторизации через Telegram
authorized_phones = [
    '+7(900)000-00-01',  # superadmin
    '+7(900)000-00-02',  # admin1
    '+7(900)000-00-03',  # brigade1
    '+7(900)000-00-04',  # warehouse1
]

# Проверка критически важных переменных окружения
def check_environment():
    """Проверка наличия критически важных переменных окружения"""
    missing_vars = []
    
    if not BOT_TOKEN:
        missing_vars.append('BOT_TOKEN')
    
    if not SUPER_GROUP_ID:
        missing_vars.append('SUPER_GROUP_ID')
    
    if missing_vars:
        print(f"⚠️  ПРЕДУПРЕЖДЕНИЕ: Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("   Telegram бот может не работать корректно.")
        print("   Добавьте их в настройках Render.com Dashboard.")
        return False
    
    print("✅ Все переменные окружения настроены корректно")
    return True

# Проверка при импорте модуля
if __name__ != '__main__':
    check_environment()
