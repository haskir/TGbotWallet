from .imports import *

payment_router: Router = Router()


@payment_router.message(StateFilter(FSMewPayment), Text(text="Отмена"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Ну, ладно",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@payment_router.message(StateFilter(FSMewPayment.FSMFillCategory), F.text.isalpha(),
                        ~Text(text="Назад",
                              ignore_case=True))
async def new_payment_category(message: Message, state: FSMContext):
    await message.answer(text="Введите название магазина",
                         reply_markup=default_keyboard.as_markup())
    udb.get_user(message.from_user.id).state["Category"] = message.text
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), F.text.isalpha(),
                        ~Text(text="Назад",
                              ignore_case=True))
async def new_payment_total(message: Message, state: FSMContext):
    await message.answer(text="Сколько потратили?")
    udb.get_user(message.from_user.id).state["Market"] = message.text
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), F.text.isdigit())
async def new_payment_description(message: Message, state: FSMContext):
    await message.answer(text="Введите описание")
    udb.get_user(message.from_user.id).state["Total"] = message.text
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.message(StateFilter(FSMewPayment.FSMFillDescription),
                        ~Text(text="Назад", ignore_case=True))
async def new_payment_check(message: Message, state: FSMContext):
    udb.get_user(message.from_user.id).state["Description"] = message.text
    await message.answer(text=f"Всё верно?",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text='\n'.join(udb.get_user(message.from_user.id).state.values()),
                         reply_markup=check_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMCheck)


@payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Да"))
async def done(message: Message, state: FSMContext):
    await message.answer("Готово!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Что будем делать дальше?",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@payment_router.message(StateFilter(FSMewPayment.FSMFillCategory), Text(text="Назад", ignore_case=True))
async def back1(message: Message, state: FSMContext):
    await state.set_state(FSMMenuState)
    await message.answer(text="Ну, ладно",
                         reply_markup=check_keyboard.as_markup(),
                         resize_keyboard=True)
    await message.answer(text="Что будем делать дальше?",
                         reply_markup=menu_keyboard.as_markup())


@payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), Text(text="Назад", ignore_case=True))
async def back2(message: Message, state: FSMContext):
    await message.answer(text="Введите категорию траты")
    await state.set_state(FSMewPayment.FSMFillCategory)


@payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), Text(text="Назад", ignore_case=True))
async def back3(message: Message, state: FSMContext):
    await message.answer(text="Введите название магазина")
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.message(StateFilter(FSMewPayment.FSMFillDescription), Text(text="Назад", ignore_case=True))
async def back4(message: Message, state: FSMContext):
    await message.answer(text="Сколько потратили?")
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Назад"))
async def back5(message: Message, state: FSMContext):
    await message.answer(text="Введите описание")
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.message(StateFilter(FSMewPayment))
async def echo(message: Message, state: FSMContext):
    await message.answer("Моя твоя не понимать")
