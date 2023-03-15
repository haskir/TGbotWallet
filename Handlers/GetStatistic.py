from .imports import *

get_statistic_router: Router = Router()

statistic_states: dict = {
    "ShowEverything": [FSMGetStatistic.FSMGetStatisticMenu, "Что теперь?"],
    "StatisticByDate": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не умею сортировать по дате"],
    "StatisticByCategory": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не умею сортировать по категории"],
    "StatisticByTotal": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не научился сортировать по сумме"],
    "DeletePaymentByUid": [FSMGetStatistic.FSMDeletePaymentsByUid, "Введите uid покупки"]
}


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetStatisticMenu))
async def statistic_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data not in statistic_states:
        return
    if "ShowEverything" in callback.data:
        await show_all_payments(callback, state)
    await callback.message.answer(text=statistic_states.get(callback.data)[1],
                                  reply_markup=default_keyboard.as_markup())
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


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByCategory))
async def statistic_by_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByTotal))
async def statistic_by_total(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)


@get_statistic_router.message(StateFilter(FSMGetStatistic),
                              Text(text="Назад", ignore_case=True))
async def enrollment_delete(message: Message, state: FSMContext):
    await message.answer(text="Что будем делать?",
                         reply_markup=statistic_keyboard.as_markup())
    await state.set_state(FSMGetStatistic.FSMGetStatisticMenu)
