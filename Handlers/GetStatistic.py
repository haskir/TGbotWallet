from .imports import *


get_statistic_router: Router = Router()


@get_statistic_router.callback_query(StateFilter(FSMGetStatistic),
                                   lambda callback: callback.data == "GetStatistic")
async def get_statistic_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Извини, это пока ещё недопилено")
    await state.set_state(FSMMenuState)