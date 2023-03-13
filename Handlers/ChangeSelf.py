from .imports import *

change_self_router: Router = Router()

change_self_states: dict = {
    "ChangeSelfEmail": [FSMChangeSelf.FSMChangeSelfMenu, "Я ещё не научился изменять e-mail"],
    "ChangeSelfName": [FSMChangeSelf.FSMChangeSelfMenu, "Я ещё не научился изменять имя"],
    "ChangeSelfInfo": [FSMChangeSelf.FSMChangeSelfMenu, "Я ещё не научился показывать информацию о пользователе"]
}


@change_self_router.callback_query(StateFilter(FSMChangeSelf.FSMChangeSelfMenu))
async def change_self_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=change_self_states.get(callback.data)[1],
                                  reply_markup=default_keyboard.as_markup())
    await state.set_state(change_self_states.get(callback.data)[0])


@change_self_router.callback_query(StateFilter(FSMChangeSelf.FSMChangeEmail))
async def change_self_email(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@change_self_router.callback_query(StateFilter(FSMChangeSelf.FSMChangeName))
async def change_self_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@change_self_router.callback_query(StateFilter(FSMChangeSelf.FSMShowInfo))
async def change_self_info(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@change_self_router.message(StateFilter(FSMChangeSelf.FSMChangeSelfMenu),
                            Text(text="Назад", ignore_case=True))
async def enrollment_delete(message: Message, state: FSMContext):
    await message.answer(text="Возвращаю обратно, в главное меню",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Что будем делать?",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)
