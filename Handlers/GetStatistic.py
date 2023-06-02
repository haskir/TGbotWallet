from Workers import bot
from .imports import *
from aiogram.types import BufferedInputFile
from asyncio import sleep

get_statistic_router: Router = Router()

statistic_states = {
    "ShowEverything": [FSMGetStatistic.FSMGetStatisticMenu, "Что теперь?", statistic_keyboard],
    "StatisticByDate": [FSMGetStatistic.FSMGetByDate, "Сортировка по дате", months_keyboard],
    "StatisticByCategory": [FSMGetStatistic.FSMGetByCategory, "Сортировка по категории", categories_keyboard],
    "StatisticByTotal": [FSMGetStatistic.FSMGetByTotal, "Введите нужный диапазон через тире\n"
                                                        "Например: 0 - 1000", default_keyboard],
    "DeletePaymentByUid": [FSMGetStatistic.FSMDeletePaymentsByUid, "Введите uid покупки", default_keyboard]
}


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic),
                                     lambda call: call.data == "Back" or call.data == "Cancel")
async def back_to_statistic_menu(callback: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Получить статистику",
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetStatisticMenu))
async def statistic_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data == "ShowEverything":
        await show_all_payments(callback)
        return

    await bot.edit_message_text(text=statistic_states.get(callback.data)[1],
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=statistic_states.get(callback.data)[2].as_markup())
    await state.set_state(statistic_states.get(callback.data)[0])


async def show_all_payments(callback: CallbackQuery):
    file_in_bytes = await googleHandler.download_sheet(udb.get_user(callback.from_user.id).sheet_id)
    user_sheet = BufferedInputFile(file_in_bytes, f"{callback.from_user.username}.xlsx")
    await bot.send_document(chat_id=callback.message.chat.id,
                            document=user_sheet)
    await callback.message.answer(text="Тут все ваши траты!",
                                  reply_markup=statistic_keyboard.as_markup())


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMDeletePaymentsByUid), F.text.isdigit())
async def delete_payment_by_uid_correct(message: Message, state: FSMContext):
    bot_message = await message.answer(text=f"Удаляем...\n")
    while True:
        for k in range(1, 4):
            await bot.edit_message_text(text="Удаляем" + "." * k,
                                        message_id=bot_message.message_id,
                                        chat_id=bot_message.chat.id)
            await sleep(1)
        if await delete_payment(message.from_user.id, udb, payments_handler, message.text):
            await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)
            await bot.edit_message_text(text="Успешно удалено!",
                                        message_id=bot_message.message_id,
                                        chat_id=bot_message.chat.id,
                                        reply_markup=statistic_keyboard.as_markup())
            return
        else:
            await bot.edit_message_text(text="Такого id нет в ваших покупках, попробуйте ещё раз!",
                                        message_id=bot_message.message_id,
                                        chat_id=bot_message.chat.id,
                                        reply_markup=default_keyboard.as_markup())
            return


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMDeletePaymentsByUid))
async def delete_payment_by_uid_incorrect(message: Message, state: FSMContext):
    await bot.delete_message(message_id=message.message_id,
                             chat_id=message.chat.id)
    await message.answer(text="Вы ввели что-то непонятное, пожалуйста, введите число",
                         reply_markup=default_keyboard.as_markup())


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByDate))
async def statistic_by_date(callback: CallbackQuery, state: FSMContext):
    date_from, date_to = parse_dates(callback)
    only_summary = False
    if "202" in callback.data:
        only_summary = True
    result = show_payments(callback.from_user.id, udb,
                           payments_handler,
                           sort=[payments_handler.DATESORT, (date_from, date_to)],
                           only_summary=only_summary)
    await callback.message.answer(text=result,
                                  reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic),
                                     lambda callback: callback.data in default_categories)
async def statistic_by_category(callback: CallbackQuery, state: FSMContext):
    result = show_payments(
        user=callback.from_user.id,
        user_database=udb,
        payments_handler=payments_handler,
        sort=[payments_handler.CATEGORYSORT, (callback.data,)]
    )
    await bot.edit_message_text(text=f"Вот, что я смог найти:\n{result}\nЧто дальше?",
                                message_id=callback.message.message_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMGetByTotal),
                              parse_total)
async def statistic_by_total_correct(message: Message, state: FSMContext):
    result = show_payments(
        user=message.from_user.id,
        user_database=udb,
        payments_handler=payments_handler,
        sort=[payments_handler.TOTALSORT, parse_total(message)]
    )
    await message.answer(text=f"Вот, что я смог найти\n{result}\nЧто дальше?",
                         reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMGetByTotal))
async def statistic_by_total_incorrect(message: Message, state: FSMContext):
    await message.answer(text="Моя твоя не понимать, повтори")
    await state.set_state(FSMGetStatistic.FSMGetByTotal)
