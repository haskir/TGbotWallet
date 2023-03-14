from Handlers.imports import *
from aiogram.types import Message, CallbackQuery
from Services.Dataclasses import *
from Services.Interfaces.PaymentsGoogleSheet import PaymentsGoogleSheet


def create_sheet_for_new_user(user: User) -> str:
    drive_handler = GoogleDriver()
    user.sheet_id = drive_handler.create(str(user.uid))
    user.permission_id = drive_handler.create_permission(user.sheet_id, user.email)
    return user.sheet_id


def email_validation(email: str | Message) -> bool:
    from re import compile, fullmatch

    email = email.text if isinstance(email, Message) else email

    regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if fullmatch(regex, email):
        return True
    else:
        return False


def show_user(user: User):
    return "\n".join(map(str, [user.uid, user.inner_name, user.email]))


def add_payment(user_uid: str | int, user_database: UserDatabase, payments_handler: PaymentsGoogleSheet):
    if isinstance(user_uid, int):
        user_uid = str(user_uid)
    user = user_database.get_user(user_uid)
    payments_handler.write(user.sheet_id, Payment(None, None, *user.state.values()))


async def back_to_menu(callback: CallbackQuery, state: FSMContext) -> bool:
    if "BackToMainMenu" in callback.data:
        await callback.message.answer(text="Возвращаюсь",
                                      reply_markup=menu_keyboard.as_markup())
        await state.set_state(FSMMenuState)
        return True
    return False