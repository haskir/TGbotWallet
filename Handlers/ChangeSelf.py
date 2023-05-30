from .imports import *
from Services.Functions import *

change_self_router: Router = Router()

change_self_states: dict = {
    "ChangeSelfEmail": [FSMChangeSelf.FSMChangeEmail, "Введите новый Email адрес"],
    "ChangeSelfName": [FSMChangeSelf.FSMChangeName, "Введите новое имя"],
    "ChangeSelfInfo": [FSMChangeSelf.FSMChangeSelfMenu, "Посмотрим...\n"]
}


@change_self_router.callback_query(StateFilter(FSMChangeSelf.FSMChangeSelfMenu))
async def change_self_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data not in change_self_states:
        return
    if callback.data == "ChangeSelfInfo":
        await callback.message.answer(
            text=f"Вот, что я о вас знаю: \n{show_user(udb.get_user(callback.from_user.id))}",
            reply_markup=change_self_keyboard.as_markup())
        return

    await callback.message.answer(text=change_self_states.get(callback.data)[1],
                                  reply_markup=default_keyboard.as_markup())
    await state.set_state(change_self_states.get(callback.data)[0])


@change_self_router.message(StateFilter(FSMChangeSelf.FSMChangeEmail),
                            lambda email: email_validation(email))
async def change_self_email_correct(message: Message, state: FSMContext):
    user = udb.get_user(message.from_user.id)
    user.email = message.text
    user.permission_id = googleHandler.create_permission(user.sheet_id, message.text)
    await message.answer(text=f"Изменено: \n{show_user(udb.get_user(message.from_user.id))}",
                         reply_markup=change_self_keyboard.as_markup())
    udb_g_sheet.update_user(user)
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@change_self_router.message(StateFilter(FSMChangeSelf.FSMChangeEmail))
async def change_self_email_incorrect(message: Message, state: FSMContext):
    await message.answer("Что-то не похоже на e-mail, повторите")
    await state.set_state(FSMChangeSelf.FSMChangeEmail)


@change_self_router.message(StateFilter(FSMChangeSelf.FSMChangeName), F.text.isalpha())
async def change_self_name_correct(message: Message, state: FSMContext):
    user = udb.get_user(message.from_user.id)
    user.inner_name = message.text.capitalize()
    await message.answer(text=f"Изменено: \n{show_user(udb.get_user(message.from_user.id))}",
                         reply_markup=change_self_keyboard.as_markup())
    udb_g_sheet.update_user(user)
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)


@change_self_router.message(StateFilter(FSMChangeSelf.FSMChangeName))
async def change_self_name_incorrect(message: Message, state: FSMContext):
    await message.answer("Что-то не похоже на имя, повторите")
    await state.set_state(FSMChangeSelf.FSMChangeName)


@change_self_router.callback_query(StateFilter(FSMChangeSelf), lambda call: "Back" in call.data)
async def change_self_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=change_self_keyboard.as_markup())
    await state.set_state(FSMChangeSelf.FSMChangeSelfMenu)