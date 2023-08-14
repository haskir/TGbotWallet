from .imports import *
from Services.UserStates import FSMEnrollment

enrollment_router: Router = Router()

enrollment_states: dict = {
    "FSMFillCategory": [
        FSMEnrollment.FSMFillCategory,
        "Выберите категорию",
        ],
    "FSMFillTotal": [
        FSMEnrollment.FSMFillTotal,
        "Введите сумму"
    ],
    "FSMCheck": [
        FSMEnrollment.FSMCheck,
        "Всё верно?"
    ]
}


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMFillCategory),
                                  lambda call: call.data in enrollment_categories)
async def enrollment_category(callback: CallbackQuery, state: FSMContext):
    await state.set_data(
        {
            "Category": "Пополнение",
            "Market": callback.data,
            "Total": 0,
            "Description": callback.data,

        }
    )
    # Следующее состояние - вписывание суммы
    await bot.edit_message_text(text=enrollment_states.get("FSMFillTotal")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=default_keyboard.as_markup())
    await state.set_state(enrollment_states.get("FSMFillTotal")[0])


@enrollment_router.message(StateFilter(FSMEnrollment.FSMFillTotal),
                           lambda total: total.text.isdigit())
async def enrollment_total(message: Message, state: FSMContext):
    # Вписал сумму в "пользователя"
    await state.update_data(
        {
            "Total": message.text,
        }
    )
    # Следующее состояние - проверка правильности пользователем данных
    result = await state.get_data()
    text = f"{enrollment_states.get('FSMCheck')[1]} \n{result['Description']} - {result['Total']} руб."
    await message.answer(
        text=text,
        reply_markup=check_keyboard.as_markup()
    )
    await state.set_state(enrollment_states.get("FSMCheck")[0])


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMCheck),
                                  lambda call: call.data == "Yes")
async def done(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        text="Главное меню",
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=menu_keyboard.as_markup()
    )
    result = await state.get_data()
    await state.set_data({})
    await add_payment(udb.get_user(callback.from_user.id), result, payments_handler)
    await state.set_state(FSMMenuState)


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMCheck),
                                  lambda call: call.data == "Back")
# Check -> Total
async def back1(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        text=enrollment_states.get("FSMFillTotal")[1],
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=default_keyboard.as_markup()
    )
    await state.set_state(FSMEnrollment.FSMFillTotal)


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMFillTotal),
                                  lambda call: call.data == "Back")
#  Total -> Category
async def back2(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        text=enrollment_states.get("FSMFillCategory")[1],
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=enrollment_keyboard.as_markup()
    )
    await state.set_state(FSMEnrollment.FSMFillCategory)


@enrollment_router.callback_query(lambda call: call.data == "Cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenuState)
    await state.set_data({})
    await bot.edit_message_text(
        text="Главное меню",
        message_id=callback.message.message_id,
        chat_id=callback.message.chat.id,
        reply_markup=menu_keyboard.as_markup()
    )


@enrollment_router.message(StateFilter(FSMEnrollment))
async def echo(message: Message, state: FSMContext):
    await message.answer("Моя твоя не понимать")
