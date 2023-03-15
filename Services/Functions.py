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


def show_payments(user: User | str | int,
                  user_database: UserDatabase,
                  payments_handler: PaymentsGoogleSheet,
                  sort: None | list = None) -> str:

    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    all_payments = payments_handler.show_all(sheet_id)
    if sort is not None:
        print(f"{sort=}\n{all_payments=}")
        all_payments = sort[0](all_payments[:], sort[1])
    if all_payments:
        result = [Payment(*string) for string in all_payments]
        return "\n".join(str(payment) for payment in result)
    else:
        return"Пока что пусто\n"


def delete_payment(user: User | str | int,
                   user_database: UserDatabase,
                   payments_handler: PaymentsGoogleSheet,
                   payment: str | int) -> bool:
    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    return payments_handler.delete_payment(sheet_id, payment)
