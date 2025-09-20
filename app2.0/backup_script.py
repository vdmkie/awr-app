#!/usr/bin/env python3
"""
Скрипт автоматического резервного копирования данных AWR
Создает архив с JSON файлами и фотографиями
"""

import os
import shutil
import json
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def create_backup():
    """Создание резервной копии всех данных"""
    
    try:
        # Создание папки для бэкапов
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Формирование имени архива с временной меткой
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'awr_backup_{timestamp}'
        backup_path = os.path.join(backup_dir, backup_name)
        
        # Создание временной папки для сборки бэкапа
        temp_backup_dir = f'{backup_path}_temp'
        os.makedirs(temp_backup_dir, exist_ok=True)
        
        # Копирование JSON файлов данных
        data_dir = 'data'
        if os.path.exists(data_dir):
            shutil.copytree(data_dir, os.path.join(temp_backup_dir, 'data'))
            logging.info("Скопированы файлы данных")
        
        # Копирование загруженных фотографий
        uploads_dir = 'uploads'
        if os.path.exists(uploads_dir):
            shutil.copytree(uploads_dir, os.path.join(temp_backup_dir, 'uploads'))
            logging.info("Скопированы загруженные файлы")
        
        # Копирование важных конфигурационных файлов
        config_files = ['config.py', 'requirements.txt', 'README.md']
        for config_file in config_files:
            if os.path.exists(config_file):
                shutil.copy2(config_file, temp_backup_dir)
        
        # Создание архива
        shutil.make_archive(backup_path, 'zip', temp_backup_dir)
        
        # Удаление временной папки
        shutil.rmtree(temp_backup_dir)
        
        # Информация о созданном бэкапе
        backup_size = os.path.getsize(f'{backup_path}.zip') / (1024 * 1024)  # MB
        logging.info(f"Бэкап создан: {backup_path}.zip ({backup_size:.2f} MB)")
        
        # Очистка старых бэкапов (сохраняем только последние 7)
        cleanup_old_backups(backup_dir)
        
        return True
        
    except Exception as e:
        logging.error(f"Ошибка создания бэкапа: {e}")
        return False

def cleanup_old_backups(backup_dir, keep_count=7):
    """Удаление старых бэкапов, оставляем только последние keep_count"""
    
    try:
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.startswith('awr_backup_') and file.endswith('.zip'):
                file_path = os.path.join(backup_dir, file)
                backup_files.append((file_path, os.path.getctime(file_path)))
        
        # Сортировка по времени создания (новые первыми)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Удаление старых файлов
        if len(backup_files) > keep_count:
            for file_path, _ in backup_files[keep_count:]:
                os.remove(file_path)
                logging.info(f"Удален старый бэкап: {os.path.basename(file_path)}")
                
    except Exception as e:
        logging.error(f"Ошибка очистки старых бэкапов: {e}")

def get_backup_info():
    """Получение информации о доступных бэкапах"""
    
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        return []
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('awr_backup_') and file.endswith('.zip'):
            file_path = os.path.join(backup_dir, file)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            created = datetime.fromtimestamp(os.path.getctime(file_path))
            
            backups.append({
                'filename': file,
                'path': file_path,
                'size_mb': round(size_mb, 2),
                'created': created.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    backups.sort(key=lambda x: x['created'], reverse=True)
    return backups

def restore_backup(backup_file):
    """Восстановление из резервной копии"""
    
    try:
        if not os.path.exists(backup_file):
            logging.error(f"Файл бэкапа не найден: {backup_file}")
            return False
        
        # Создание резервной копии текущих данных перед восстановлением
        current_backup_name = f"current_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logging.info("Создание резервной копии текущих данных...")
        create_backup()
        
        # Извлечение архива во временную папку
        temp_restore_dir = 'temp_restore'
        shutil.unpack_archive(backup_file, temp_restore_dir)
        
        # Восстановление данных
        if os.path.exists(os.path.join(temp_restore_dir, 'data')):
            if os.path.exists('data'):
                shutil.rmtree('data')
            shutil.move(os.path.join(temp_restore_dir, 'data'), 'data')
            logging.info("Восстановлены файлы данных")
        
        # Восстановление загруженных файлов
        if os.path.exists(os.path.join(temp_restore_dir, 'uploads')):
            if os.path.exists('uploads'):
                shutil.rmtree('uploads')
            shutil.move(os.path.join(temp_restore_dir, 'uploads'), 'uploads')
            logging.info("Восстановлены загруженные файлы")
        
        # Очистка временной папки
        shutil.rmtree(temp_restore_dir)
        
        logging.info(f"Восстановление из {backup_file} завершено успешно")
        return True
        
    except Exception as e:
        logging.error(f"Ошибка восстановления: {e}")
        return False

if __name__ == "__main__":
    print("=== AWR Backup Manager ===")
    print("1. Создать бэкап")
    print("2. Показать список бэкапов")
    print("3. Восстановить из бэкапа")
    
    choice = input("Выберите действие (1-3): ")
    
    if choice == "1":
        print("Создание бэкапа...")
        if create_backup():
            print("✅ Бэкап создан успешно!")
        else:
            print("❌ Ошибка создания бэкапа")
    
    elif choice == "2":
        backups = get_backup_info()
        if backups:
            print("\nДоступные бэкапы:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['filename']} ({backup['size_mb']} MB) - {backup['created']}")
        else:
            print("Бэкапы не найдены")
    
    elif choice == "3":
        backups = get_backup_info()
        if backups:
            print("\nВыберите бэкап для восстановления:")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup['filename']} - {backup['created']}")
            
            try:
                selection = int(input("Номер бэкапа: ")) - 1
                if 0 <= selection < len(backups):
                    confirm = input(f"Восстановить из {backups[selection]['filename']}? (y/N): ")
                    if confirm.lower() == 'y':
                        if restore_backup(backups[selection]['path']):
                            print("✅ Восстановление завершено!")
                        else:
                            print("❌ Ошибка восстановления")
                    else:
                        print("Отменено")
                else:
                    print("Неверный номер")
            except ValueError:
                print("Неверный ввод")
        else:
            print("Бэкапы не найдены")
    
    else:
        print("Неверный выбор")
