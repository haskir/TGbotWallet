# from Handlers.imports import *
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
                  # sort = [function_to_sort, (start: int | str, stop: None | int | str)]
                  sort: None | list[callable, tuple] = None) -> str:
    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    all_payments: list[Payment] = payments_handler.sheetHandler.last_row(sheet_id)
    if sort is not None:
        all_payments = payments_handler.sort(sheet_id,
                                             sort[0],
                                             sort[1])
    if all_payments:
        result = [Payment(*string) for string in payments_handler.show_all(sheet_id)]
        return "\n".join(str(payment) for payment in result)
    else:
        return "Пока что пусто\n"


def delete_payment(user: User | str | int,
                   user_database: UserDatabase,
                   payments_handler: PaymentsGoogleSheet,
                   payment: str | int) -> bool:
    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    return payments_handler.delete_payment(sheet_id, payment)


def __delete_empty_spaces(string: str) -> str:
    from re import sub
    return sub(" +", " ", string)


def parse_total(message: Message):
    message = __delete_empty_spaces(message.text) if isinstance(message, Message) else __delete_empty_spaces(message)
    try:
        if "-" in message:
            start, stop = list(map(int, message.split("-")))
        else:
            start, stop = list(map(int, message.split(" ")))
    except Exception as e:
        print(e)
        return False
    else:
        return start, stop if stop > start else False
