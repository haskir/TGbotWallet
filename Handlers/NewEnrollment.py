from .imports import *

new_enrollment_router: Router = Router()


@new_enrollment_router.callback_query(StateFilter(FSMNewEnrollment))
# lambda callback: callback.data == "NewEnrollment")
async def get_statistic_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Извини, это пока ещё недопилено",
                          reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)
