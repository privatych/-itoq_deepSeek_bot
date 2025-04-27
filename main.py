import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from config import BOT_TOKEN, ADMIN_ID
from admin_router import admin_router
from user_router import user_router
from services import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Инициализация базы данных
    await init_db()
    logger.info("База данных успешно инициализирована")

    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # Запуск бота
    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}") 