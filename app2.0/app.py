from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import json
from datetime import datetime
import pandas as pd
import logging
from data_manager import DataManager
from config import USERS, SECRET_KEY, UPLOADS_DIR, WORK_TYPES, TASK_STATUSES, BRIGADE_STATUSES

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max file size (уменьшено для стабильности)
app.config['SESSION_COOKIE_SECURE'] = False  # Установите True при использовании HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

dm = DataManager()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Проверка разрешенных форматов файлов"""
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

def validate_file_size(file):
    """Проверка размера файла"""
    file.seek(0, 2)  # Перейти к концу файла
    size = file.tell()
    file.seek(0)  # Вернуться к началу
    return size <= 2 * 1024 * 1024  # 2MB максимум

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def role_required(roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if 'user' not in session or session['user']['role'] not in roles:
                flash('Недостаточно прав доступа')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and check_password_hash(USERS[username]['password'], password):
            session['user'] = {
                'username': username,
                'role': USERS[username]['role'],
                'name': USERS[username]['name']
            }
            logging.info(f'Успешный вход пользователя: {username}')
            return redirect(url_for('dashboard'))
        else:
            logging.warning(f'Неудачная попытка входа: {username}')
            flash('Неверный логин или пароль')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_role = session['user']['role']
    return render_template(f'dashboard_{user_role}.html', user=session['user'])

# Маршруты для Супер-админа и Админов
@app.route('/new_task', methods=['GET', 'POST'])
@login_required
@role_required(['super_admin', 'admin'])
def new_task():
    if request.method == 'POST':
        task_data = {
            'address': request.form['address'],
            'floors': int(request.form['floors']),
            'entrances': int(request.form['entrances']),
            'work_type': request.form['work_type'],
            'description': request.form['description'],
            'access_info': request.form['access_info'],
            'urgent': 'urgent' in request.form,
            'created_by': session['user']['name']
        }
        
        if 'assigned_brigade' in request.form and request.form['assigned_brigade']:
            task_data['assigned_brigade'] = request.form['assigned_brigade']
            task_data['status'] = 'В работе'
        
        if 'assigned_admin' in request.form and request.form['assigned_admin']:
            task_data['assigned_admin'] = request.form['assigned_admin']
            task_data['status'] = 'В работе'
        
        task_id = dm.add_task(task_data)
        flash(f'Задача #{task_id} успешно создана')
        return redirect(url_for('task_list'))
    
    brigades = dm.load_data('brigades')
    access_info = dm.load_data('access_info')
    return render_template('new_task.html', 
                         work_types=WORK_TYPES, 
                         brigades=brigades,
                         access_info=access_info,
                         user=session['user'])

@app.route('/task_list')
@login_required
def task_list():
    tasks = dm.load_data('tasks')
    user_role = session['user']['role']
    user_name = session['user']['name']
    
    # Фильтрация задач в зависимости от роли
    if user_role == 'brigade':
        tasks = [task for task in tasks if task.get('assigned_brigade') == user_name]
    elif user_role == 'admin':
        # Админы видят все задачи кроме личных заданий от супер-админа
        tasks = [task for task in tasks if not task.get('assigned_admin')]
    
    return render_template('task_list.html', tasks=tasks, user=session['user'])

@app.route('/my_tasks')
@login_required
def my_tasks():
    user_role = session['user']['role']
    user_name = session['user']['name']
    
    if user_role == 'admin':
        tasks = dm.get_admin_tasks(user_name)
    elif user_role == 'brigade':
        tasks = dm.get_brigade_tasks(user_name)
        # Разделяем на активные, выполненные и отложенные
        active_tasks = [t for t in tasks if t['status'] == 'В работе']
        completed_tasks = [t for t in tasks if t['status'] == 'Выполнено']
        postponed_tasks = [t for t in tasks if t['status'] == 'Отложено']
        
        return render_template('brigade_tasks.html', 
                             active_tasks=active_tasks,
                             completed_tasks=completed_tasks,
                             postponed_tasks=postponed_tasks,
                             user=session['user'])
    else:
        tasks = []
    
    return render_template('my_tasks.html', tasks=tasks, user=session['user'])

@app.route('/task/<int:task_id>')
@login_required
def task_detail(task_id):
    tasks = dm.load_data('tasks')
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        flash('Задача не найдена')
        return redirect(url_for('task_list'))
    
    reports = dm.load_data('reports')
    task_reports = [r for r in reports if r.get('task_id') == task_id]
    
    return render_template('task_detail.html', task=task, reports=task_reports, user=session['user'])

@app.route('/task/<int:task_id>/report', methods=['GET', 'POST'])
@login_required
@role_required(['brigade'])
def task_report(task_id):
    tasks = dm.load_data('tasks')
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task or task.get('assigned_brigade') != session['user']['name']:
        flash('Нет прав на эту задачу')
        return redirect(url_for('my_tasks'))
    
    if request.method == 'POST':
        report_data = {
            'task_id': task_id,
            'brigade': session['user']['name'],
            'comment': request.form.get('comment', ''),
            'access': request.form.get('access', ''),
            'photos': [],
            'materials': []
        }
        
        # Обработка фотографий
        uploaded_files = request.files.getlist('photos')
        failed_uploads = []
        
        for file in uploaded_files:
            if file and file.filename:
                if not allowed_file(file.filename):
                    failed_uploads.append(f'"{file.filename}" - неподдерживаемый формат')
                    continue
                    
                if not validate_file_size(file):
                    failed_uploads.append(f'"{file.filename}" - слишком большой файл (>макс 2MB)')
                    continue
                    
                try:
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    
                    # Создать папку, если её нет
                    photos_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'photos')
                    os.makedirs(photos_dir, exist_ok=True)
                    
                    file_path = os.path.join(photos_dir, filename)
                    file.save(file_path)
                    report_data['photos'].append(filename)
                    logging.info(f'Файл успешно загружен: {filename}')
                except Exception as e:
                    failed_uploads.append(f'"{file.filename}" - ошибка загрузки')
                    logging.error(f'Ошибка загрузки файла {file.filename}: {e}')
        
        if failed_uploads:
            flash(f'Не удалось загрузить: {"; ".join(failed_uploads)}', 'warning')
        
        # Обработка списания материалов
        materials_data = request.form.getlist('material_name')
        quantities = request.form.getlist('material_quantity')
        
        for material, quantity in zip(materials_data, quantities):
            if material and quantity:
                report_data['materials'].append({
                    'name': material,
                    'quantity': float(quantity)
                })
        
        dm.add_report(report_data)
        
        # Проверяем полноту отчета
        report_complete = all([
            report_data['comment'],
            report_data['access'],
            len(report_data['photos']) > 0,
            len(report_data['materials']) > 0
        ])
        
        if report_complete:
            # Отмечаем задачу как выполненную
            dm.update_task(task_id, {'status': 'Выполнено'})
            flash('Отчет полный, задача отмечена как выполненная')
        else:
            flash('Отчет сохранен, но не все поля заполнены')
        
        return redirect(url_for('my_tasks'))
    
    materials = dm.load_data('materials')
    brigade_materials = dm.load_data('brigade_materials')
    user_materials = brigade_materials.get(session['user']['name'], {})
    
    return render_template('task_report.html', 
                         task=task, 
                         materials=materials,
                         user_materials=user_materials,
                         user=session['user'])

# Маршруты для кладовщика
@app.route('/warehouse')
@login_required
@role_required(['warehouse'])
def warehouse():
    return render_template('warehouse.html', user=session['user'])

@app.route('/materials')
@login_required
def materials():
    materials = dm.load_data('materials')
    brigade_materials = dm.load_data('brigade_materials')
    return render_template('materials.html', 
                         materials=materials,
                         brigade_materials=brigade_materials,
                         user=session['user'])

@app.route('/reports')
@login_required
def reports():
    reports = dm.load_data('reports')
    return render_template('reports.html', reports=reports, user=session['user'])

@app.route('/map')
@login_required
def map_view():
    tasks = dm.load_data('tasks')
    user_role = session['user']['role']
    user_name = session['user']['name']
    
    if user_role == 'brigade':
        # Бригады видят только свои задачи в работе
        tasks = [t for t in tasks if t.get('assigned_brigade') == user_name and t['status'] == 'В работе']
    
    return render_template('map.html', tasks=tasks, user=session['user'])

@app.route('/brigades')
@login_required
@role_required(['super_admin', 'admin'])
def brigades_list():
    brigades = dm.load_data('brigades')
    return render_template('brigades.html', brigades=brigades, statuses=BRIGADE_STATUSES, user=session['user'])

# API маршруты
@app.route('/api/tasks')
@login_required
def api_tasks():
    tasks = dm.load_data('tasks')
    return jsonify(tasks)

if __name__ == '__main__':
    # Создание необходимых директорий
    os.makedirs('data', exist_ok=True)
    os.makedirs('uploads/photos', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    
    # Проверка конфигурации
    from config import BOT_TOKEN
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logging.warning("ВНИМАНИЕ: Не настроен токен бота. Обновите config.py")
    
    logging.info("🚀 Запуск AWR Web Application")
    logging.info(f"🌐 Приложение доступно по адресу: http://0.0.0.0:5000")
    
    # Получить настройки из переменных окружения
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    port = int(os.getenv('PORT', 5000))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
