from Workers import bot

from .imports import *

menu_router: Router = Router()

states = {
    "NewPayment": [FSMewPayment.FSMFillCategory, "Введите категорию траты", categories_keyboard],
    "NewEnrollment": [FSMEnrollment.FSMFillCategory, "Выберите категорию пополнения", enrollment_keyboard],
    "GetStatistic": [FSMGetStatistic.FSMGetStatisticMenu, "Статистика", statistic_keyboard],
    "ChangeSelf": [FSMChangeSelf.FSMChangeSelfMenu, "Профиль", change_self_keyboard]
}


@menu_router.callback_query(StateFilter(FSMMenuState))
async def go_from_menu_to(callback: CallbackQuery, state: FSMContext):
    if callback.data in states.keys():
        await bot.edit_message_text(text=states.get(callback.data)[1],
                                    message_id=callback.message.message_id,
                                    chat_id=callback.message.chat.id)
        await callback.message.edit_reply_markup(reply_markup=states.get(callback.data)[2].as_markup())
        await state.set_state(states.get(callback.data)[0])


@menu_router.callback_query(lambda callback: "BackToMainMenu" in callback.data)
async def back_from_any(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@menu_router.message(Command(commands=['showudb']))
async def show_udb(message: Message, state: FSMContext):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        await message.answer(text=str(udb.database))
    else:
        await message.answer(text="Не покажу.")
