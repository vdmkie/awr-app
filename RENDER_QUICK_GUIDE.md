# 🚀 Быстрая шпаргалка: Развертывание AWR на Render.com

## 📝 Чек-лист развертывания (30 минут)

### ✅ 1. GitHub репозиторий (5 минут)
- [ ] Создать репозиторий на GitHub
- [ ] Загрузить код приложения
- [ ] Заменить файлы: `cp config_render.py config.py && cp bot_render.py bot.py`
- [ ] Добавить `render.yaml` в корень

### ✅ 2. Telegram бот (5 минут)
- [ ] Создать бота через @BotFather
- [ ] Получить BOT_TOKEN
- [ ] Создать группу и добавить бота
- [ ] Получить SUPER_GROUP_ID

### ✅ 3. Render.com настройка (10 минут)
- [ ] Зарегистрироваться на Render.com
- [ ] Подключить GitHub аккаунт
- [ ] Создать Web Service из репозитория
- [ ] Добавить переменные окружения

### ✅ 4. Переменные окружения
```
BOT_TOKEN=1234567890:AAAA...
SUPER_GROUP_ID=-1001234567890
SECRET_KEY=your-super-secret-key-32-chars
FLASK_ENV=production
PORT=5000
```

### ✅ 5. Проверка (10 минут)
- [ ] Открыть URL приложения
- [ ] Войти как superadmin/admin123
- [ ] Протестировать Telegram бота
- [ ] Проверить логи в Render

## 🔗 Полезные ссылки

- **Render.com:** https://render.com
- **GitHub:** https://github.com
- **BotFather:** https://t.me/botfather
- **Получить GROUP_ID:** `https://api.telegram.org/bot<TOKEN>/getUpdates`

## 📞 Учетные записи

- superadmin / admin123
- admin1 / admin123  
- brigade1 / brigade123
- warehouse1 / warehouse123

## 🆘 Решение проблем

**Проблема:** Приложение не запускается
- Проверить логи в Render Dashboard
- Убедиться, что все переменные окружения добавлены

**Проблема:** Telegram бот не работает
- Проверить BOT_TOKEN и SUPER_GROUP_ID
- Убедиться, что бот добавлен в группу как администратор

**Проблема:** Ошибка авторизации
- Проверить номера телефонов в authorized_phones
- Убедиться, что пользователь в авторизованной группе

## 💰 Стоимость

- **Free Tier:** $0/месяц (ограничения)
- **Starter:** $7/месяц (рекомендуется)

---
*⏱️ Общее время развертывания: 30-60 минут*