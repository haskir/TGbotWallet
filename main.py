from Handlers import *
import os
import dotenv

dotenv.load_dotenv()

API_TOKEN: str = os.getenv('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)
dp.include_router(change_self_router)
dp.include_router(get_statistic_router)
dp.include_router(menu_router)
dp.include_router(new_enrollment_router)
dp.include_router(new_payment_router)
dp.include_router(registration_router)

if __name__ == '__main__':
    dp.run_polling(bot)
    ...
# Запускаем бота
