from .imports import *
from Services.Functions import *


payment_router: Router = Router()

payment_states: dict = {
    "NewPaymentCategory": [FSMewPayment.FSMFillCategory, "Выберите категорию траты"],
    "NewPaymentMarket": [FSMewPayment.FSMFillMarket, "Введите название магазина"],
    "NewPaymentTotal": [FSMewPayment.FSMFillTotal, "Сколько потратили?"],
    "NewPaymentDescription": [FSMewPayment.FSMFillDescription, "Введите описание"],
    "NewPaymentCheck": [FSMewPayment.FSMCheck, "Всё верно?"],
    "MainMenu": [FSMMenuState, "Готово!"],
    "Cancel": [FSMewPayment.FSMFillCategory, "Ну, назад так назад"],
}


@payment_router.message(StateFilter(FSMewPayment), Text(text="Отмена"))
async def cancel(message: Message, state: FSMContext):
    await message.answer("Ну, ладно",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillCategory))
async def new_payment_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=payment_states.get("NewPaymentMarket")[1],
                                  reply_markup=default_keyboard.as_markup())
    udb.get_user(callback.from_user.id).state["Category"] = callback.data
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), F.text.isalpha(),
                        ~Text(text="Назад",
                              ignore_case=True))
async def new_payment_total(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentTotal")[1])
    udb.get_user(message.from_user.id).state["Market"] = message.text
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), F.text.isdigit())
async def new_payment_description(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentDescription")[1])
    udb.get_user(message.from_user.id).state["Total"] = message.text
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.message(StateFilter(FSMewPayment.FSMFillDescription),
                        ~Text(text="Назад", ignore_case=True))
async def new_payment_check(message: Message, state: FSMContext):
    udb.get_user(message.from_user.id).state["Description"] = message.text
    await message.answer(text=payment_states.get("NewPaymentCheck")[1],
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text='\n'.join(udb.get_user(message.from_user.id).state.values()),
                         reply_markup=check_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMCheck)


@payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Да"))
async def done(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("MainMenu")[1],
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Что будем делать дальше?",
                         reply_markup=menu_keyboard.as_markup())
    add_payment(message.from_user.id, udb, payments_handler)
    await state.set_state(FSMMenuState)


@payment_router.message(StateFilter(FSMewPayment.FSMFillCategory), Text(text="Назад", ignore_case=True))
async def back1(message: Message, state: FSMContext):
    await state.set_state(FSMMenuState)
    await message.answer(text=payment_states.get("Cancel")[1],
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Главное меню",
                         reply_markup=menu_keyboard.as_markup())


@payment_router.message(StateFilter(FSMewPayment.FSMFillMarket), Text(text="Назад", ignore_case=True))
async def back2(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentCategory")[1])
    await state.set_state(FSMewPayment.FSMFillCategory)


@payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), Text(text="Назад", ignore_case=True))
async def back3(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentMarket")[1])
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.message(StateFilter(FSMewPayment.FSMFillDescription), Text(text="Назад", ignore_case=True))
async def back4(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentTotal")[1])
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.message(StateFilter(FSMewPayment.FSMCheck), Text(text="Назад"))
async def back5(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentDescription")[1],
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.message(StateFilter(FSMewPayment))
async def echo(message: Message, state: FSMContext):
    await message.answer("Моя твоя не понимать")
