import os, asyncio, asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL","http://localhost:5173")
DATABASE_URL = os.getenv("DATABASE_URL","postgresql://postgres:postgres@localhost:5432/awr")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def db():
    return await asyncpg.connect(DATABASE_URL)

@dp.message(CommandStart())
async def start(m: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить телефон", request_contact=True)]],
        resize_keyboard=True
    )
    await m.answer("Привет! Отправь свой номер телефона для авторизации.", reply_markup=kb)

@dp.message(F.contact)
async def on_contact(m: Message):
    phone = m.contact.phone_number
    user_id = m.from_user.id
    async with await db() as conn:
        # сверяем номер с базой (по users.phone)
        row = await conn.fetchrow("SELECT id, role FROM users WHERE phone=$1", phone)
        if not row:
            await m.answer("Номер не найден в базе. Обратитесь к администратору.")
            return
        # записываем tg_id если пустой
        await conn.execute("UPDATE users SET tg_id=$1 WHERE id=$2 AND (tg_id IS NULL OR tg_id='')", str(user_id), row['id'])

    open_btn = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Открыть приложение", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True
    )
    await m.answer("Готово! Нажми кнопку, чтобы открыть мини-приложение.", reply_markup=open_btn)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
