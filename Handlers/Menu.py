import os

from .imports import *

menu_router: Router = Router()

states = {
    "NewPayment": [FSMewPayment.FSMFillCategory, "Введите категорию траты", categories_keyboard],
    "NewEnrollment": [FSMEnrollment.FSMCEnrollmentMenu, "Вот, что мы можем сделать:", enrollment_keyboard],
    "GetStatistic": [FSMGetStatistic.FSMGetStatisticMenu, "Укажите нужный вам фильтр", statistic_keyboard],
    "ChangeSelf": [FSMChangeSelf.FSMChangeSelfMenu, "Профиль", change_self_keyboard]
}


@menu_router.callback_query(StateFilter(FSMMenuState))
async def go_from_menu_to(callback: CallbackQuery, state: FSMContext):
    if callback.data in states.keys():
        await state.set_state(states.get(callback.data)[0])
        await callback.message.edit_reply_markup(reply_markup=states.get(callback.data)[2].as_markup(
            resize_keyboard=True))


@menu_router.message(~StateFilter(default_state, FSMMenuState), Text(text="Отмена", ignore_case=True))
async def process_cancel_command_state(message: Message, state: FSMContext):
    user = udb.get_user(message.from_user.id)
    if user and user.email != "EMPTY_VALUE":
        await message.answer(text='Что мы умеем:',
                             reply_markup=menu_keyboard.as_markup())
        await state.set_state(FSMMenuState)
    else:
        await message.answer("Главное меню",
                             reply_markup=menu_keyboard.as_markup(one_time_keyboard=True))
        await state.set_state(FSMFillForm.fill_name)


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
