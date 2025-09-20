# 🚀 Пошаговая инструкция развертывания AWR на Render.com

## 📋 Предварительные требования

- ✅ Аккаунт GitHub
- ✅ Аккаунт Render.com (бесплатный)
- ✅ Telegram Bot Token
- ✅ Telegram Group ID для авторизации

---

## 🔧 Шаг 1: Подготовка GitHub репозитория

### 1.1 Создание репозитория
1. Откройте [GitHub.com](https://github.com)
2. Нажмите **"New"** или **"+"** → **"New repository"**
3. Заполните:
   - **Repository name:** `awr-management-app`
   - **Description:** `AWR Work Management Application`
   - ✅ **Public** (или Private - на ваш выбор)
   - ✅ **Add a README file**
4. Нажмите **"Create repository"**

### 1.2 Загрузка кода приложения
```bash
# 1. Клонируйте созданный репозиторий
git clone https://github.com/YOUR_USERNAME/awr-management-app.git
cd awr-management-app

# 2. Извлеките архив приложения в папку репозитория
# (скачайте и распакуйте AWR_Application_Final_*.zip)

# 3. Добавьте все файлы в git
git add .
git commit -m "Initial commit: AWR Management Application"
git push origin main
```

---

## 🌐 Шаг 2: Настройка Render.com

### 2.1 Создание аккаунта и подключение GitHub
1. Откройте [Render.com](https://render.com)
2. Нажмите **"Get Started for Free"**
3. Войдите через **GitHub** аккаунт
4. Подтвердите разрешения для Render

### 2.2 Создание Web Service
1. В Dashboard нажмите **"New +"** → **"Web Service"**
2. Выберите **"Build and deploy from a Git repository"**
3. Найдите и выберите репозиторий `awr-management-app`
4. Нажмите **"Connect"**

---

## ⚙️ Шаг 3: Конфигурация Web Service

### 3.1 Основные настройки
```
Name: awr-management-app
Region: Frankfurt (EU Central) [или ближайший к вам]
Branch: main
Root Directory: [оставить пустым]
Runtime: Python 3
```

### 3.2 Build & Deploy настройки
```
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

### 3.3 Instance Type
- **Free Tier** (для тестирования)
- **Starter** ($7/месяц - рекомендуется для продакшена)

---

## 🔑 Шаг 4: Переменные окружения

### 4.1 Добавление Environment Variables
В разделе **"Environment"** добавьте:

```bash
# Основные настройки
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here-32-characters-long

# Telegram Bot настройки
BOT_TOKEN=your-telegram-bot-token
SUPER_GROUP_ID=your-telegram-group-id

# Порт для Render
PORT=5000

# Режим продакшена
PRODUCTION=true
```

### 4.2 Получение Telegram данных

#### BOT_TOKEN:
1. Откройте Telegram
2. Найдите [@BotFather](https://t.me/botfather)
3. Отправьте `/newbot`
4. Следуйте инструкциям
5. Скопируйте полученный token

#### SUPER_GROUP_ID:
1. Создайте группу в Telegram
2. Добавьте бота в группу как администратора
3. Отправьте сообщение в группу
4. Откройте: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. Найдите `"chat":{"id":-XXXXXXXXX}` - это ваш GROUP_ID

---

## 🛠️ Шаг 5: Модификация кода для Render

### 5.1 Обновление app.py
Создайте файл в репозитории с изменениями:

```python
# В конце app.py замените:
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 5.2 Создание render.yaml (опционально)
```yaml
services:
  - type: web
    name: awr-management-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: PORT
        value: 5000
```

---

## 🚀 Шаг 6: Развертывание

### 6.1 Запуск деплоя
1. Нажмите **"Create Web Service"**
2. Дождитесь завершения Build (5-10 минут)
3. Проверьте логи на наличие ошибок

### 6.2 Проверка URL
После успешного деплоя вы получите URL вида:
```
https://awr-management-app.onrender.com
```

---

## 🤖 Шаг 7: Настройка Telegram бота

### 7.1 Создание отдельного сервиса для бота
1. В Render Dashboard: **"New +"** → **"Background Worker"**
2. Выберите тот же репозиторий
3. Настройки:
   ```
   Name: awr-telegram-bot
   Start Command: python bot.py
   ```
4. Добавьте те же Environment Variables

### 7.2 Альтернатива: Webhook вместо polling
Обновите bot.py для использования webhook:
```python
# В bot.py замените polling на webhook
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

async def main():
    # Настройка webhook
    webhook_url = f"https://your-app.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    
    # Запуск веб-сервера для webhook
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    return app

if __name__ == '__main__':
    web.run_app(main(), host='0.0.0.0', port=8080)
```

---

## 🔍 Шаг 8: Проверка и тестирование

### 8.1 Проверка веб-приложения
1. Откройте URL вашего приложения
2. Попробуйте войти с тестовыми данными:
   - `superadmin` / `admin123`
3. Проверьте основные функции

### 8.2 Проверка Telegram бота
1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Введите номер телефона из authorized_phones
4. Проверьте получение кода авторизации

### 8.3 Мониторинг логов
В Render Dashboard:
- **"Logs"** - просмотр логов в реальном времени
- **"Metrics"** - мониторинг производительности

---

## 🛡️ Шаг 9: Настройки безопасности и продакшена

### 9.1 Custom Domain (опционально)
1. В настройках сервиса → **"Settings"**
2. **"Custom Domains"** → **"Add"**
3. Введите ваш домен
4. Настройте DNS записи

### 9.2 Мониторинг и уведомления
1. **"Settings"** → **"Notifications"**
2. Настройте уведомления на email/Slack
3. Включите **"Health Checks"**

### 9.3 Автоматические бэкапы
Render не предоставляет persistent storage, поэтому:
1. Настройте backup в cloud storage (AWS S3, Google Cloud)
2. Используйте scheduled jobs для регулярных бэкапов

---

## 💡 Шаг 10: Полезные команды и советы

### 10.1 Локальная отладка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Установка переменных окружения
export BOT_TOKEN="your-token"
export SUPER_GROUP_ID="your-group-id"

# Запуск локально
python app.py
```

### 10.2 Обновление приложения
```bash
git add .
git commit -m "Update: описание изменений"
git push origin main
# Render автоматически перезапустит сервис
```

### 10.3 Отладка проблем
- **Логи:** Render Dashboard → "Logs"
- **Health Checks:** добавьте `/health` endpoint
- **Environment Variables:** проверьте правильность значений

---

## 📞 Готовые учетные записи

После успешного деплоя используйте:
- **superadmin** / **admin123** - Суперадминистратор
- **admin1** / **admin123** - Администратор
- **brigade1** / **brigade123** - Бригадир
- **warehouse1** / **warehouse123** - Кладовщик

---

## 🎯 Результат

После выполнения всех шагов у вас будет:
- ✅ Работающее веб-приложение на `https://your-app.onrender.com`
- ✅ Telegram бот для авторизации
- ✅ Автоматические деплои при push в GitHub
- ✅ Мониторинг и логирование
- ✅ SSL сертификат (автоматически)

**Время развертывания:** 30-60 минут  
**Стоимость:** Бесплатно (или $7/месяц для Starter)

---

*Разработано: MiniMax Agent | Дата: 20.09.2025*