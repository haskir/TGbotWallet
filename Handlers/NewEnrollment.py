from .imports import *
from Services.UserStates import FSMEnrollment

enrollment_router: Router = Router()

enrollment_states: dict = {
    "EnrollmentShow": [FSMEnrollment.FSMCEnrollmentMenu, "Я ещё не научился показывать историю"],
    "EnrollmentNew": [FSMEnrollment.FSMCEnrollmentMenu, "Я ещё не научился добавлять"],
    "EnrollmentDelete": [FSMEnrollment.FSMCEnrollmentMenu, "Я ещё не научился удалять"]
}


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMCEnrollmentMenu))
async def enrollment_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data not in enrollment_states:
        return
    await callback.message.answer(text=enrollment_states.get(callback.data)[1],
                                  reply_markup=default_keyboard.as_markup())
    await state.set_state(enrollment_states.get(callback.data)[0])


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMEnrollmentShow))
async def enrollment_show(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMEnrollment.FSMCEnrollmentMenu)


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMEnrollmentNew))
async def enrollment_new(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMEnrollment.FSMCEnrollmentMenu)


@enrollment_router.callback_query(StateFilter(FSMEnrollment.FSMCEnrollmentDelete))
async def enrollment_delete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMEnrollment.FSMCEnrollmentMenu)

