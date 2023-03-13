from .imports import *

new_payment_router: Router = Router()


@new_payment_router.message(StateFilter(FSMewPayment), Text(text="Отмена"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Ну, ладно",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillCategory), F.text.isalpha(),
                            ~Text(text="Назад",
                            ignore_case=True))
async def new_payment_category(message: Message, state: FSMContext):
    await message.answer(text="Введите название магазина",
                         reply_markup=default_keyboard.as_markup())
    udb.get_user(message.from_user.id).state["Category"] = message.text
    await state.set_state(FSMewPayment.FSMFillMarket)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), F.text.isalpha(),
                            ~Text(text="Назад",
                            ignore_case=True))
async def new_payment_total(message: Message, state: FSMContext):
    await message.answer(text="Сколько потратили?")
    udb.get_user(message.from_user.id).state["Market"] = message.text
    await state.set_state(FSMewPayment.FSMFillTotal)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), F.text.isdigit())
async def new_payment_description(message: Message, state: FSMContext):
    await message.answer(text="Введите описание")
    udb.get_user(message.from_user.id).state["Total"] = message.text
    await state.set_state(FSMewPayment.FSMFillDescription)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillDescription),
                            F.text.isalpha(),
                            ~Text(text="Назад", ignore_case=True))
async def new_payment_check(message: Message, state: FSMContext):
    default_keyboard.add(check_button)
    udb.get_user(message.from_user.id).state["Description"] = message.text
    await message.answer(text=f"Всё верно?\n" + '\n'.join(udb.get_user(message.from_user.id).state.values()),
                         reply_markup=default_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMCheck)


@new_payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Да"))
async def done(message: Message, state: FSMContext):
    await message.answer("Готово!",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@new_payment_router.callback_query(StateFilter(FSMewPayment.FSMFillCategory),
                                   lambda callback_data: callback_data.data == "Back")
async def back1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenuState)
    await callback.answer(text="Что будем делать дальше?",
                          reply_markup=ReplyKeyboardRemove(),
                          resize_keyboard=True)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), Text(text="Назад", ignore_case=True))
async def back2(message: Message, state: FSMContext):
    await message.answer(text="Введите категорию траты")
    await state.set_state(FSMewPayment.FSMFillCategory)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), Text(text="Назад", ignore_case=True))
async def back3(message: Message, state: FSMContext):
    await message.answer(text="Введите название магазина")
    await state.set_state(FSMewPayment.FSMFillMarket)


@new_payment_router.message(StateFilter(FSMewPayment.FSMFillDescription), Text(text="Назад", ignore_case=True))
async def back4(message: Message, state: FSMContext):
    await message.answer(text="Сколько потратили?")
    await state.set_state(FSMewPayment.FSMFillTotal)


@new_payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Назад"))
async def back5(message: Message, state: FSMContext):
    await message.answer(text="Введите описание")
    await state.set_state(FSMewPayment.FSMFillDescription)


@new_payment_router.message(StateFilter(FSMewPayment))
async def echo(message: Message, state: FSMContext):
    await message.answer("Моя твоя не понимать")
