import asyncio
from aiogram.types.error_event import ErrorEvent
from Handlers import *

# Создаем объекты бота и диспетчера
from Workers import bot

storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage, )
dp.include_router(profile_router)
dp.include_router(get_statistic_router)
dp.include_router(menu_router)
dp.include_router(enrollment_router)
dp.include_router(payment_router)
dp.include_router(registration_router)


@dp.callback_query(~StateFilter(default_state),
                   lambda callback: "BackToMainMenu" in callback.data)
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@dp.errors()
async def back_to_menu_error(error: ErrorEvent, state: FSMContext):
    print(error)


# reload_router = Router()
#
#
# @reload_router.callback_query()
# async def on_reboot_any_button(callback: CallbackQuery, state: FSMContext):
#     await callback.message.answer(text="У нас что-то пошло не так",
#                                   reply_markup=menu_keyboard.as_markup())
#     await state.set_state(FSMMenuState)
#
#
# dp.include_router(reload_router)


async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        dp.shutdown()
        return


# Запускаем бота
if __name__ == '__main__':
    while True:
        asyncio.run(main())
