from .imports import *

menu_router: Router = Router()

states = {
    "NewPayment": [FSMewPayment.FSMFillCategory, "Введите категорию траты", default_keyboard],
    "NewEnrollment": [FSMEnrollment.FSMCEnrollmentMenu, "Вот, что мы можем сделать:", enrollment_keyboard],
    "GetStatistic": [FSMGetStatistic.FSMGetStatisticMenu, "Укажите нужный вам фильтр", statistic_keyboard],
    "ChangeSelf": [FSMChangeSelf.FSMChangeSelfMenu, "Профиль", change_self_keyboard]
}


# start_button = KeyboardButton(text="/start")
# start_keyboard = ReplyKeyboardBuilder([[start_button]])


@menu_router.callback_query(StateFilter(FSMMenuState))
async def go_from_menu_to(callback: CallbackQuery, state: FSMContext):
    if callback.data in states.keys():
        await state.set_state(states.get(callback.data)[0])
        await callback.message.answer(states.get(callback.data)[1],
                                      reply_markup=states.get(callback.data)[2].as_markup(one_time_keyboard=True))


@menu_router.message(StateFilter(default_state, FSMMenuState), Text(text="Отмена", ignore_case=True))
async def cancel_command(message: Message):
    await message.answer(text='Отменять нечего')


@menu_router.message(StateFilter(default_state, FSMMenuState), Text(text="Назад", ignore_case=True))
async def back_command(message: Message):
    await message.answer(text='Некуда отступать')


@menu_router.message(~StateFilter(default_state, FSMMenuState), Text(text="Отмена", ignore_case=True))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Отменяем...',
                         reply_markup=ReplyKeyboardRemove())
    user = udb.get_user(message.from_user.id)
    if user and user.email != "EMPTY_VALUE":
        await message.answer(text='Что мы умеем:',
                             reply_markup=menu_keyboard.as_markup())
        await state.set_state(FSMMenuState)
    else:
        await message.answer("Что мы умеем:",
                             reply_markup=menu_keyboard.as_markup(one_time_keyboard=True))
        await state.set_state(FSMMenuState)


@menu_router.callback_query(lambda callback: "BackToMainMenu" in callback.data)
async def back_from_any(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Возвращаю",
                                  reply_markup=ReplyKeyboardRemove())
    await callback.message.answer(text="Что будем делать?",
                                  reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)
