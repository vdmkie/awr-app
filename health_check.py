#!/usr/bin/env python3
"""
Скрипт проверки работоспособности AWR приложения
Проверяет ключевые компоненты системы
"""

import os
import json
import requests
import sys
from datetime import datetime

def check_files():
    """Проверка наличия необходимых файлов"""
    required_files = [
        'app.py',
        'bot.py', 
        'config.py',
        'data_manager.py',
        'requirements.txt',
        'templates/base.html',
        'templates/login.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Отсутствуют файлы:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Все необходимые файлы найдены")
        return True

def check_directories():
    """Проверка необходимых директорий"""
    required_dirs = [
        'data',
        'uploads',
        'uploads/photos',
        'templates'
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ Создана директория: {dir_path}")
            except Exception as e:
                print(f"❌ Ошибка создания директории {dir_path}: {e}")
                return False
    
    print("✅ Все необходимые директории готовы")
    return True

def check_config():
    """Проверка конфигурации"""
    try:
        from config import BOT_TOKEN, USERS, AUTHORIZED_PHONES
        
        issues = []
        
        # Проверка токена бота
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            issues.append("Не настроен токен Telegram бота (BOT_TOKEN)")
        
        # Проверка пользователей
        if not USERS:
            issues.append("Не настроены пользователи системы")
        
        # Проверка авторизованных телефонов
        if not AUTHORIZED_PHONES:
            issues.append("Не настроены авторизованные номера телефонов")
        
        if issues:
            print("⚠️  Проблемы конфигурации:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ Конфигурация корректна")
            return True
            
    except ImportError as e:
        print(f"❌ Ошибка импорта конфигурации: {e}")
        return False

def check_data_files():
    """Проверка файлов данных"""
    try:
        from data_manager import DataManager
        dm = DataManager()
        
        # Проверка создания начальных данных
        tasks = dm.load_data('tasks')
        materials = dm.load_data('materials')
        
        print("✅ Файлы данных инициализированы корректно")
        print(f"   - Задачи: {len(tasks) if isinstance(tasks, list) else 'инициализированы'}")
        print(f"   - Материалы: {len(materials) if isinstance(materials, dict) else 'инициализированы'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки файлов данных: {e}")
        return False

def check_web_app(port=5000):
    """Проверка доступности веб-приложения"""
    try:
        url = f"http://localhost:{port}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Веб-приложение доступно на {url}")
            return True
        else:
            print(f"⚠️  Веб-приложение отвечает с кодом {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"⚠️  Веб-приложение не запущено на порту {port}")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки веб-приложения: {e}")
        return False

def check_dependencies():
    """Проверка зависимостей Python"""
    try:
        import flask
        import aiogram
        import pandas
        import werkzeug
        print("✅ Все Python зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("Выполните: pip install -r requirements.txt")
        return False

def run_full_check():
    """Полная проверка системы"""
    print("=== Проверка системы AWR ===")
    print(f"Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    checks = [
        ("Файлы приложения", check_files),
        ("Директории", check_directories),
        ("Python зависимости", check_dependencies),
        ("Конфигурация", check_config),
        ("Файлы данных", check_data_files),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        result = check_func()
        results.append(result)
    
    # Проверка веб-приложения (опционально)
    print(f"\n--- Веб-приложение ---")
    web_result = check_web_app()
    if not web_result:
        print("ℹ️  Для проверки веб-приложения запустите: python app.py")
    
    print(f"\n=== Результат проверки ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 Все проверки пройдены успешно!")
        print("Система готова к работе!")
        return True
    else:
        print(f"⚠️  Пройдено {passed} из {total} проверок")
        print("Исправьте указанные проблемы перед запуском")
        return False

def quick_fix():
    """Быстрое исправление основных проблем"""
    print("=== Быстрое исправление ===")
    
    # Создание директорий
    dirs_created = 0
    required_dirs = ['data', 'uploads', 'uploads/photos', 'backups']
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            dirs_created += 1
            print(f"✅ Создана: {dir_path}")
    
    if dirs_created == 0:
        print("✅ Все директории уже существуют")
    
    # Инициализация данных
    try:
        from data_manager import DataManager
        dm = DataManager()
        print("✅ Файлы данных инициализированы")
    except Exception as e:
        print(f"❌ Ошибка инициализации данных: {e}")
    
    print("Исправление завершено!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        quick_fix()
    else:
        success = run_full_check()
        if not success:
            print("\nДля автоматического исправления запустите:")
            print("python health_check.py --fix")
