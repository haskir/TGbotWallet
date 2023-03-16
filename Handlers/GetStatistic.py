from .imports import *

get_statistic_router: Router = Router()

statistic_states: dict = {
    "ShowEverything": [FSMGetStatistic.FSMGetStatisticMenu, "Что теперь?"],
    "StatisticByDate": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не умею сортировать по дате"],
    "StatisticByCategory": [FSMGetStatistic.FSMChoosingCategory, "Сортировка по категории", categories_keyboard],
    "StatisticByTotal": [FSMGetStatistic.FSMGetByTotal, "Введите нужный диапазон через тире\n"
                                                        "Например: 0 - 1000"],
    "DeletePaymentByUid": [FSMGetStatistic.FSMDeletePaymentsByUid, "Введите uid покупки"]
}


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetStatisticMenu))
async def statistic_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data not in statistic_states:
        return
    if "ShowEverything" == callback.data:
        await show_all_payments(callback, state)

    temp_keyboard = default_keyboard \
        if len(statistic_states.get(callback.data)) < 3 \
        else statistic_states.get(callback.data)[2]

    await callback.message.answer(text=statistic_states.get(callback.data)[1],
                                  reply_markup=temp_keyboard.as_markup())
    await state.set_state(statistic_states.get(callback.data)[0])


async def show_all_payments(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f"Вот, что я нашёл:\n"
                                       f"{show_payments(callback.from_user.id, udb, payments_handler)}",
                                  reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMDeletePaymentsByUid), F.text.isdigit())
async def delete_payment_by_uid_correct(message: Message, state: FSMContext):
    await message.answer(text=f"Удаляем...\n")
    if delete_payment(message.from_user.id, udb, payments_handler, message.text):
        await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)
        await message.answer(text="Успешно удалено! Что дальше?",
                             reply_markup=statistic_keyboard.as_markup())
    else:
        await message.answer(text="Такого id нет в ваших покупках, попробуйте ещё раз!")


@get_statistic_router.message(StateFilter(FSMGetStatistic.FSMDeletePaymentsByUid),
                              ~Text(text="Назад", ignore_case=True),
                              ~Text(text="Отмена", ignore_case=True))
async def delete_payment_by_uid_incorrect(message: Message, state: FSMContext):
    await message.answer(text=f"Вы ввели что-то непонятное, пожалуйста, введите число")


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByDate))
async def statistic_by_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMChoosingCategory),
                                     lambda callback: callback.data in default_categories)
async def statistic_by_category(callback: CallbackQuery, state: FSMContext):
    result = show_payments(
        user=callback.from_user.id,
        user_database=udb,
        payments_handler=payments_handler,
        sort=[payments_handler.CATEGORYSORT, (callback.data, )]
    )
    await callback.message.answer(text=f"Вот, что я смог найти:\n{result}\nЧто дальше?",
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


@get_statistic_router.message(StateFilter(FSMGetStatistic),
                              Text(text="Назад", ignore_case=True))
async def enrollment_delete(message: Message, state: FSMContext):
    await message.answer(text="Что будем делать?",
                         reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)
