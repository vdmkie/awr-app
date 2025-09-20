# 🚀 Инструкция по развертыванию AWR на Render через GitHub

## Что включено в архив:
- ✅ Полное приложение AWR с исправлениями безопасности
- ✅ Хэширование паролей (werkzeug.security)
- ✅ Конфигурация для Render (render.yaml)
- ✅ Docker-файлы для контейнеризации
- ✅ Все зависимости и статические файлы
- ✅ Документация по развертыванию

## Быстрое развертывание:

### 1. Загрузка на GitHub
1. Распакуйте архив `AWR_Render_GitHub_Deploy_20250920_230120.zip`
2. Создайте новый репозиторий на GitHub
3. Загрузите все файлы в репозиторий
4. Переименуйте `GITHUB_README.md` в `README.md`

### 2. Развертывание на Render
1. Зайдите на [render.com](https://render.com)
2. Подключите GitHub аккаунт
3. Создайте **New Web Service**
4. Выберите ваш репозиторий
5. Настройки:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 3. Переменные окружения (Environment Variables)
Добавьте в Render Dashboard:
```
FLASK_ENV=production
SECRET_KEY=ваш_секретный_ключ_32_символа
PORT=5000
PRODUCTION=true
BOT_TOKEN=ваш_telegram_bot_token
SUPER_GROUP_ID=id_telegram_группы
```

### 4. Telegram бот (опционально)
Создайте **Background Worker**:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`

## 📋 Логины по умолчанию:
- **Супер-админ**: `superadmin` / `admin123`
- **Админ**: `admin` / `pass123`
- **Бригадир**: `brigade1` / `work123`
- **Кладовщик**: `warehouse` / `store123`

⚠️ **ВАЖНО**: Смените пароли после первого входа!

## 📞 Поддержка:
См. полную документацию в файле `RENDER_DEPLOYMENT_GUIDE.md`

---
Архив создан: 2025-09-20 23:01
Автор: MiniMax Agent