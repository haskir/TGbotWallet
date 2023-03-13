from .imports import *

get_statistic_router: Router = Router()

statistic_states: dict = {
    "StatisticByDate": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не умею сортировать по дате"],
    "StatisticByCategory": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не умею сортировать по категории"],
    "StatisticByTotal": [FSMGetStatistic.FSMGetStatisticMenu, "Я ещё не научился сортировать по сумме"]
}


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetStatisticMenu))
async def statistic_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=statistic_states.get(callback.data)[1],
                                  reply_markup=default_keyboard.as_markup())
    await state.set_state(statistic_states.get(callback.data)[0])


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByDate))
async def statistic_by_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByCategory))
async def statistic_by_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic.FSMGetByTotal))
async def statistic_by_total(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@get_statistic_router.message(StateFilter(FSMGetStatistic),
                            Text(text="Назад", ignore_case=True))
async def enrollment_delete(message: Message, state: FSMContext):
    await message.answer(text="Возвращаю обратно, в главное меню",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Что будем делать?",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)
