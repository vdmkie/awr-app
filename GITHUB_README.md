# AWR - Система управления рабочими ресурсами

Полнофункциональная система управления рабочими ресурсами с веб-интерфейсом и Telegram-ботом.

## 🚀 Развертывание на Render.com

### Быстрый запуск

1. **Создайте форк этого репозитория** на GitHub
2. **Войдите в [Render.com](https://render.com)** и подключите ваш GitHub аккаунт
3. **Создайте новый Web Service:**
   - Repository: выберите ваш форк
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

### Переменные окружения

Добавьте в Render Dashboard следующие Environment Variables:

```
FLASK_ENV=production
SECRET_KEY=ваш_секретный_ключ_для_flask
PORT=5000
PRODUCTION=true
BOT_TOKEN=ваш_telegram_bot_token
SUPER_GROUP_ID=id_вашей_супергруппы
```

### Telegram бот (опционально)

Для запуска Telegram бота создайте Background Worker:
- Build Command: `pip install -r requirements.txt`
- Start Command: `python bot.py`

## 📁 Структура проекта

```
├── app.py              # Основное Flask приложение
├── bot.py              # Telegram бот
├── config.py           # Конфигурация и пользователи
├── data_manager.py     # Управление данными
├── requirements.txt    # Python зависимости
├── Dockerfile         # Docker конфигурация
├── render.yaml        # Конфигурация для Render
├── templates/         # HTML шаблоны
├── static/           # CSS, JS, изображения
└── data/             # JSON файлы данных
```

## 🔐 Безопасность

- ✅ Пароли хешированы с помощью werkzeug.security
- ✅ Защищенные сессии
- ✅ Валидация загружаемых файлов
- ✅ Ограничения размера файлов

## 📖 Полная документация

См. файл `RENDER_DEPLOYMENT_GUIDE.md` для подробных инструкций по развертыванию.

## 👥 Роли пользователей

- **Super Admin**: Полный доступ к системе
- **Admin**: Управление задачами и отчетами
- **Brigade**: Выполнение задач
- **Warehouse**: Управление складом

## 🛠 Технологический стек

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Bot**: Aiogram (Telegram Bot API)
- **Database**: JSON файлы (легко мигрировать на PostgreSQL)
- **Deployment**: Render.com, Docker

---

Автор: MiniMax Agent