from .imports import *


change_self_router: Router = Router()


@change_self_router.callback_query(StateFilter(FSMChangeSelf),
                                   lambda callback: callback.data == "ChangeSelf")
async def get_statistic_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Извини, это пока ещё недопилено")
    await state.set_state(FSMMenuState)