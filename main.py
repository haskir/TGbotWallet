from Handlers import *
import os
import dotenv

dotenv.load_dotenv()

TGbotWallet_token: str = os.getenv('TGbotWallet_token')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=TGbotWallet_token)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)
dp.include_router(change_self_router)
dp.include_router(get_statistic_router)
dp.include_router(menu_router)
dp.include_router(enrollment_router)
dp.include_router(payment_router)
dp.include_router(registration_router)


@dp.callback_query(~StateFilter(default_state),
                   lambda callback: "BackToMainMenu" in callback.data)
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Возвращаюсь",
                                  reply_markup=ReplyKeyboardRemove())
    await callback.message.answer(text="Главное меню",
                                  reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


def main():
    try:
        dp.run_polling(bot)
    except Exception as e:
        dp.shutdown()
        return


# Запускаем бота
if __name__ == '__main__':
    while True:
        main()
