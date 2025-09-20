"""
Обновленный bot.py для развертывания на Render.com
Использует переменные окружения для конфигурации
"""

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Получение настроек из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPER_GROUP_ID = int(os.getenv('SUPER_GROUP_ID', '0')) if os.getenv('SUPER_GROUP_ID') else None

# Авторизованные телефоны (из config)
AUTHORIZED_PHONES = [
    '+7(900)000-00-01',  # superadmin
    '+7(900)000-00-02',  # admin1
    '+7(900)000-00-03',  # brigade1
    '+7(900)000-00-04',  # warehouse1
]

# Настройка логгинга для Render.com
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler()  # Только консольный вывод для Render
    ]
)

# Проверка конфигурации
def check_bot_config():
    """Проверка настроек бота"""
    if not BOT_TOKEN:
        logging.error("❌ Не настроен BOT_TOKEN! Установите переменную окружения в Render Dashboard")
        return False
    
    if not SUPER_GROUP_ID:
        logging.error("❌ Не настроен SUPER_GROUP_ID! Установите переменную окружения в Render Dashboard")
        return False
    
    logging.info("✅ Конфигурация бота корректна")
    return True

if not check_bot_config():
    logging.error("🚨 Бот не может запуститься без корректной конфигурации")
    exit(1)

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище авторизованных пользователей
authorized_users = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        logging.info(f"👤 Пользователь {username} (ID: {user_id}) запустил бота")
        
        # Создание клавиатуры с кнопкой для отправки номера телефона
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        
        await message.answer(
            "🏗️ <b>Добро пожаловать в AWR Management System!</b>\n\n"
            "Для авторизации в системе нажмите кнопку ниже и поделитесь своим номером телефона.\n\n"
            "📋 <i>Доступ имеют только авторизованные сотрудники.</i>",
            parse_mode="HTML",
            reply_markup=kb
        )
        
    except Exception as e:
        logging.error(f"Ошибка в cmd_start: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")

@dp.message(types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    """Обработка получения номера телефона"""
    try:
        contact = message.contact
        phone = contact.phone_number
        user_id = message.from_user.id
        username = message.from_user.username or "Unknown"
        
        logging.info(f"📱 Получен номер телефона: {phone} от пользователя {username}")
        
        # Нормализация номера телефона
        normalized_phone = phone
        if phone.startswith('8'):
            normalized_phone = '+7' + phone[1:]
        elif phone.startswith('7'):
            normalized_phone = '+' + phone
        elif not phone.startswith('+'):
            normalized_phone = '+' + phone
        
        # Проверка авторизации
        is_authorized = False
        for auth_phone in AUTHORIZED_PHONES:
            # Убираем все символы кроме цифр для сравнения
            clean_auth = ''.join(filter(str.isdigit, auth_phone))
            clean_received = ''.join(filter(str.isdigit, normalized_phone))
            
            if clean_auth.endswith(clean_received[-10:]) or clean_received.endswith(clean_auth[-10:]):
                is_authorized = True
                break
        
        if is_authorized:
            # Генерация кода авторизации
            import random
            auth_code = f"{random.randint(1000, 9999)}"
            
            # Сохранение данных пользователя
            authorized_users[user_id] = {
                'phone': normalized_phone,
                'username': username,
                'auth_code': auth_code,
                'timestamp': message.date
            }
            
            # Отправка кода в супергруппу
            if SUPER_GROUP_ID:
                try:
                    await bot.send_message(
                        SUPER_GROUP_ID,
                        f"🔐 <b>Новый запрос авторизации</b>\n\n"
                        f"👤 Пользователь: @{username}\n"
                        f"📱 Телефон: {normalized_phone}\n"
                        f"🔢 Код авторизации: <code>{auth_code}</code>\n\n"
                        f"📅 Время: {message.date.strftime('%d.%m.%Y %H:%M')}",
                        parse_mode="HTML"
                    )
                    logging.info(f"✅ Код авторизации отправлен в группу для {username}")
                except Exception as e:
                    logging.error(f"❌ Ошибка отправки в группу: {e}")
            
            # Ответ пользователю
            await message.answer(
                f"✅ <b>Номер телефона подтвержден!</b>\n\n"
                f"🔢 Ваш код авторизации: <code>{auth_code}</code>\n\n"
                f"📝 Используйте этот код для входа в веб-систему AWR.\n"
                f"⏰ Код действителен в течение 1 часа.",
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
            
        else:
            logging.warning(f"⚠️ Неавторизованная попытка доступа: {normalized_phone} от {username}")
            await message.answer(
                "❌ <b>Доступ запрещен</b>\n\n"
                "Ваш номер телефона не найден в списке авторизованных пользователей.\n\n"
                "📞 Обратитесь к администратору для получения доступа.",
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
            
    except Exception as e:
        logging.error(f"Ошибка в process_contact: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке номера телефона. Попробуйте позже.",
            reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(
        "🆘 <b>Помощь по боту AWR</b>\n\n"
        "📝 <b>Доступные команды:</b>\n"
        "/start - Начать авторизацию\n"
        "/help - Показать эту справку\n\n"
        "🔐 <b>Процесс авторизации:</b>\n"
        "1. Нажмите /start\n"
        "2. Поделитесь номером телефона\n"
        "3. Получите код авторизации\n"
        "4. Используйте код для входа в веб-систему\n\n"
        "💬 <b>Поддержка:</b> Обратитесь к администратору",
        parse_mode="HTML"
    )

async def main():
    """Главная функция запуска бота"""
    try:
        logging.info("🤖 Запуск Telegram бота AWR...")
        logging.info(f"🆔 Bot ID: {(await bot.get_me()).id}")
        logging.info(f"📱 Авторизованных номеров: {len(AUTHORIZED_PHONES)}")
        
        # Запуск polling
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logging.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logging.error(f"❌ Критическая ошибка бота: {e}")
    finally:
        await bot.session.close()
        logging.info("🔒 Сессия бота закрыта")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("👋 Завершение работы бота")
    except Exception as e:
        logging.error(f"Фатальная ошибка: {e}")
