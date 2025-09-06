# AWR — Assistant Work Resurs

Бэкенд: FastAPI + PostgreSQL • Фронтенд: React (Vite) • Бот: Aiogram

## Локальный старт (Docker Compose)
1. В корне выполните:
   ```bash
   docker compose up -d --build
   ```
2. Swagger: `http://localhost:8000/docs` → `POST /api/v1/auth/seed` — создать пользователей:
   - sa (super_admin), a1 (admin), b1/b2 (crew), sk1 (storekeeper) — пароль `1`
3. Фронт: `http://localhost:5173`
4. Бот: задайте `BOT_TOKEN` при запуске сервиса bot.

## Роли и вход
- Первый вход через бота (телефон) — сохраняем `tg_id`.
- Повторные входы из TG: WebApp → `/auth/tg_login`.
- Из веба (ПК): логин/пароль.

## Переменные окружения
- API: `DATABASE_URL`, `SECRET_KEY`, `TELEGRAM_BOT_TOKEN`, `SUPERGROUP_CHAT_ID`
- WEB: `VITE_API_URL`
- BOT: `BOT_TOKEN`, `WEBAPP_URL`, `DATABASE_URL`

## Полезные эндпоинты
- `POST /api/v1/auth/seed`
- `POST /api/v1/auth/tg_login?tg_id=`
- `POST /api/v1/reports/upsert?part=1..4`
- `GET  /api/v1/inventory/warehouse/summary`
- `GET  /api/v1/inventory/export.csv`

Удачи!
