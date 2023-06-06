from .imports import *
from Services.Functions import *
from Workers import bot

payment_router: Router = Router()

payment_states: dict = {
    "NewPaymentCategory": [FSMewPayment.FSMFillCategory, "Выберите категорию траты"],
    "NewPaymentMarket": [FSMewPayment.FSMFillMarket, "Введите название магазина"],
    "NewPaymentTotal": [FSMewPayment.FSMFillTotal, "Сколько потратили?"],
    "NewPaymentDescription": [FSMewPayment.FSMFillDescription, "Введите описание"],
    "NewPaymentCheck": [FSMewPayment.FSMCheck, "Всё верно?\n"],
    "MainMenu": [FSMMenuState, "Готово!"],
    "Cancel": [FSMewPayment.FSMFillCategory, "Ну, назад так назад"],
}


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillCategory),
                               lambda callback: callback.data in default_categories)
async def new_payment_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data({"category": callback.data})
    await bot.edit_message_text(text=payment_states.get("NewPaymentMarket")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=default_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.message(StateFilter(FSMewPayment.FSMFillMarket),
                        lambda message: message.text.isalpha())
async def new_payment_total(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentTotal")[1],
                         reply_markup=default_keyboard.as_markup())
    await state.update_data({"Market": message.text})
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.message(StateFilter(FSMewPayment.FSMFillTotal), F.text.isdigit())
async def new_payment_description(message: Message, state: FSMContext):
    await message.answer(text=payment_states.get("NewPaymentDescription")[1],
                         reply_markup=default_keyboard.as_markup())
    await state.update_data({"Total": message.text})
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.message(StateFilter(FSMewPayment.FSMFillDescription))
async def new_payment_check(message: Message, state: FSMContext):
    await state.update_data({"Description": message.text})
    result = await state.get_data()
    await message.answer(text=payment_states.get("NewPaymentCheck")[1] + '\n'.join(result.values()),
                         reply_markup=check_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMCheck)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMCheck),
                               lambda call: call.data == "Yes")
async def done(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Главное меню",
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=menu_keyboard.as_markup())
    result = await state.get_data()
    await state.set_data({})
    await add_payment(udb.get_user(callback.from_user.id), result, payments_handler)
    await state.set_state(FSMMenuState)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillCategory),
                               lambda call: call.data == "Back")
async def back1(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Главное меню",
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillMarket),
                               lambda call: call.data == "Back")
async def back2(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text=payment_states.get("NewPaymentCategory")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=categories_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMFillCategory)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillTotal),
                               lambda call: call.data == "Back")
async def back3(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text=payment_states.get("NewPaymentMarket")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=default_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMFillMarket)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMFillDescription),
                               lambda call: call.data == "Back")
async def back4(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text=payment_states.get("NewPaymentTotal")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=default_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMFillTotal)


@payment_router.callback_query(StateFilter(FSMewPayment.FSMCheck),
                               lambda call: call.data == "Back")
async def back5(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text=payment_states.get("NewPaymentDescription")[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=default_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMFillDescription)


@payment_router.callback_query(lambda call: call.data == "Cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMMenuState)
    await state.set_data({})
    await bot.edit_message_text(text="Главное меню",
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=menu_keyboard.as_markup())


@payment_router.message(StateFilter(FSMewPayment))
async def echo(message: Message, state: FSMContext):
    await message.answer("Моя твоя не понимать")
