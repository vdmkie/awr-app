import os
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")
DB_DSN = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/awr")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def get_db():
    return await asyncpg.connect(dsn=DB_DSN)

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("📱 Отправить телефон", request_contact=True)]],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать! Чтобы войти, отправьте свой номер телефона:",
        reply_markup=kb
    )

@dp.message(lambda m: m.contact)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id

    conn = await get_db()
    row = await conn.fetchrow("SELECT * FROM users WHERE phone=$1", phone)
    await conn.close()

    if row:
        if not row["tg_id"]:
            conn = await get_db()
            await conn.execute("UPDATE users SET tg_id=$1 WHERE id=$2", str(user_id), row["id"])
            await conn.close()

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🚀 Открыть приложение", web_app=WebAppInfo(url=WEBAPP_URL))]],
            resize_keyboard=True
        )
        await message.answer("✅ Телефон найден! Нажмите кнопку ниже, чтобы открыть приложение:", reply_markup=kb)
    else:
        await message.answer("❌ Ваш номер телефона не найден в системе. Обратитесь к администратору.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is required")
    asyncio.run(main())
