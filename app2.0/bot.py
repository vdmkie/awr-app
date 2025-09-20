import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config import BOT_TOKEN, AUTHORIZED_PHONES, SUPER_GROUP_ID

# Настройка логгинга
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Проверка конфигурации
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    logging.error("Не настроен токен бота! Установите BOT_TOKEN в config.py")
    exit(1)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище авторизованных пользователей
authorized_users = {}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Поделиться номером", request_contact=True)]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "👋 Добро пожаловать в AWR!\n\n"
        "🔑 Для доступа к приложению необходимо поделиться номером телефона.",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.contact is not None)
async def contact_handler(message: types.Message):
    """Обработчик получения контакта"""
    phone = message.contact.phone_number
    user_id = message.from_user.id
    
    # Убираем символ '+' если он есть
    clean_phone = phone.replace('+', '')
    
    if clean_phone in AUTHORIZED_PHONES:
        # Сохраняем авторизованного пользователя
        authorized_users[user_id] = phone
        
        # Создаем клавиатуру с кнопкой запуска приложения
        # Используем переменную окружения или localhost по умолчанию
        app_url = os.getenv('WEB_APP_URL', 'http://localhost:5000')
        webapp = WebAppInfo(url=app_url)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🚀 Запустить приложение", web_app=webapp)]
            ],
            resize_keyboard=True
        )
        
        await message.answer(
            "✅ Номер подтвержден!\n\n"
            "🚀 Нажмите на кнопку ниже, чтобы запустить AWR.",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "❌ В доступе отказано.\n\n"
            "📞 Ваш номер не найден в списке авторизованных пользователей."
        )

async def send_report_to_group(report_data, task_data):
    """Отправка отчёта в супергруппу"""
    message_text = f"""
📝 Новый отчёт

🏠 Адрес: {task_data['address']}
👥 Бригада: {report_data['brigade']}
🔧 Вид работ: {task_data['work_type']}

💬 Комментарий: {report_data['comment']}
🔑 Доступ: {report_data['access']}

📦 Материалы:
"""
    
    for material in report_data['materials']:
        message_text += f"- {material['name']}: {material['quantity']}\n"
    
    try:
        await bot.send_message(SUPER_GROUP_ID, message_text)
        
        # Отправляем фотографии
        for photo in report_data['photos']:
            photo_path = f"uploads/photos/{photo}"
            with open(photo_path, 'rb') as photo_file:
                await bot.send_photo(SUPER_GROUP_ID, photo_file)
                
    except Exception as e:
        logging.error(f"Ошибка отправки в группу: {e}")

async def main():
    """Основная функция запуска бота"""
    logging.info("Пользовательский бот AWR запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
