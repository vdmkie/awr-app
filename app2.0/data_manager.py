import json
import os
from datetime import datetime
from config import DATA_DIR, USERS

class DataManager:
    def __init__(self):
        self.data_files = {
            'tasks': f'{DATA_DIR}/tasks.json',
            'reports': f'{DATA_DIR}/reports.json',
            'materials': f'{DATA_DIR}/materials.json',
            'tools': f'{DATA_DIR}/tools.json',
            'brigade_materials': f'{DATA_DIR}/brigade_materials.json',
            'brigade_tools': f'{DATA_DIR}/brigade_tools.json',
            'warehouse_log': f'{DATA_DIR}/warehouse_log.json',
            'access_info': f'{DATA_DIR}/access_info.json',
            'acceptance': f'{DATA_DIR}/acceptance.json',
            'brigades': f'{DATA_DIR}/brigades.json'
        }
        self._init_data_files()
    
    def _init_data_files(self):
        """Инициализация файлов данных с базовой структурой"""
        default_data = {
            'tasks': [],
            'reports': [],
            'materials': {
                "Кабель ВОК 4 100": 1000,
                "БО/16 100": 500,
                "Шпаклёвка 100": 200
            },
            'tools': {
                "Перфоратор проводной SN001": 1,
                "Перфоратор беспроводной SN002": 1,
                "Аккумулятор 6 ампер SN003": 5
            },
            'brigade_materials': {},
            'brigade_tools': {},
            'warehouse_log': [],
            'access_info': [],
            'acceptance': [],
            'brigades': self._get_initial_brigades()
        }
        
        for key, file_path in self.data_files.items():
            if not os.path.exists(file_path):
                self.save_data(key, default_data[key])
    
    def _get_initial_brigades(self):
        """Получить начальный список бригад из конфигурации"""
        brigades = []
        for username, user_data in USERS.items():
            if user_data['role'] == 'brigade':
                brigades.append({
                    'id': username,
                    'name': user_data['name'],
                    'phone': user_data['phone'],
                    'status': 'в работе',
                    'login': username,
                    'password': user_data['password']
                })
        return brigades
    
    def load_data(self, data_type):
        """Загрузка данных из JSON файла"""
        try:
            with open(self.data_files[data_type], 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_data(self, data_type, data):
        """Сохранение данных в JSON файл"""
        with open(self.data_files[data_type], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task_data):
        """Добавление новой задачи"""
        tasks = self.load_data('tasks')
        task_data['id'] = len(tasks) + 1
        task_data['created_date'] = datetime.now().isoformat()
        task_data['status'] = 'Новая задача'
        tasks.append(task_data)
        self.save_data('tasks', tasks)
        return task_data['id']
    
    def update_task(self, task_id, update_data):
        """Обновление задачи"""
        tasks = self.load_data('tasks')
        for task in tasks:
            if task['id'] == task_id:
                task.update(update_data)
                if 'status' in update_data:
                    if update_data['status'] == 'В работе' and 'assigned_date' not in task:
                        task['assigned_date'] = datetime.now().isoformat()
                    elif update_data['status'] == 'Выполнено' and 'completed_date' not in task:
                        task['completed_date'] = datetime.now().isoformat()
                break
        self.save_data('tasks', tasks)
    
    def add_report(self, report_data):
        """Добавление отчета"""
        reports = self.load_data('reports')
        report_data['id'] = len(reports) + 1
        report_data['created_date'] = datetime.now().isoformat()
        reports.append(report_data)
        self.save_data('reports', reports)
        return report_data['id']
    
    def get_brigade_tasks(self, brigade_name):
        """Получение задач конкретной бригады"""
        tasks = self.load_data('tasks')
        return [task for task in tasks if task.get('assigned_brigade') == brigade_name]
    
    def get_admin_tasks(self, admin_name):
        """Получение задач конкретного админа"""
        tasks = self.load_data('tasks')
        return [task for task in tasks if task.get('assigned_admin') == admin_name]
    
    def update_materials(self, material_name, quantity, operation='add'):
        """Обновление количества материалов на складе"""
        materials = self.load_data('materials')
        if material_name in materials:
            if operation == 'add':
                materials[material_name] += quantity
            else:
                materials[material_name] = max(0, materials[material_name] - quantity)
        else:
            materials[material_name] = quantity if operation == 'add' else 0
        self.save_data('materials', materials)
    
    def transfer_material_to_brigade(self, material_name, quantity, brigade_name):
        """Передача материала бригаде"""
        # Списать со склада
        self.update_materials(material_name, quantity, 'subtract')
        
        # Добавить бригаде
        brigade_materials = self.load_data('brigade_materials')
        if brigade_name not in brigade_materials:
            brigade_materials[brigade_name] = {}
        if material_name not in brigade_materials[brigade_name]:
            brigade_materials[brigade_name][material_name] = 0
        brigade_materials[brigade_name][material_name] += quantity
        self.save_data('brigade_materials', brigade_materials)
        
        # Записать в лог
        self.add_warehouse_log({
            'type': 'ТМЦ',
            'operation': 'Выдача бригаде',
            'item': material_name,
            'quantity': quantity,
            'brigade': brigade_name,
            'date': datetime.now().isoformat()
        })
    
    def add_warehouse_log(self, log_entry):
        """Добавление записи в лог склада"""
        logs = self.load_data('warehouse_log')
        log_entry['id'] = len(logs) + 1
        logs.append(log_entry)
        self.save_data('warehouse_log', logs)
