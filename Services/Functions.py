# from Handlers.imports import *
import datetime

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


async def add_payment(user: User, data: dict, payments_handler: PaymentsGoogleSheet):
    await payments_handler.write(user.sheet_id, Payment(None, None, *data.values()))


def show_payments(user: User | str | int,
                  user_database: UserDatabase,
                  payments_handler: PaymentsGoogleSheet,
                  sort: None | list[callable, tuple[str | int | datetime.date]] = None,
                  only_summary: bool = False) -> str:
    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    last_row: int = payments_handler.sheetHandler.last_row(sheet_id)
    if last_row:
        result = [Payment(*string) for string in payments_handler.show_payments(sheet_id)]

        if sort is not None:
            result = payments_handler.sort(sheet_id,
                                           sort[0],
                                           sort[1])
        if result and not only_summary:
            return __cut_big_output("".join(str(payment) for payment in result) + "\n" + __summary(result))
        if result and only_summary:
            return __summary(result)
        else:
            return "Ничего не нашёл :("
    else:
        return "Ничего не нашёл :("


async def delete_payment(user: User | str | int,
                         user_database: UserDatabase,
                         payments_handler: PaymentsGoogleSheet,
                         payment: str | int) -> bool:
    sheet_id = user_database.get_user(user).sheet_id if isinstance(user, str | int) else user.sheet_id
    return await payments_handler.delete_payment(sheet_id, payment)


def __delete_empty_spaces(string: str) -> str:
    from re import sub
    return sub(" +", " ", string)


def parse_total(message: Message | str) -> bool | tuple:
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


def __summary(list_of_payments: list[Payment]) -> None | str:
    if not list_of_payments:
        return

    categories = dict()
    for payment in list_of_payments:
        if payment.category not in categories.keys():
            categories[payment.category] = payment.total
        else:
            categories[payment.category] += payment.total
    return "\n".join(f"{key} - {value}" for key, value in categories.items()) + \
           f"\nПотрачено суммарно: {sum(categories.values())}"


def parse_dates(callback: CallbackQuery) -> None | tuple:
    from calendar import monthrange
    from datetime import datetime, timedelta
    if "Last30" == callback.data:
        date_from = datetime.today().date() - timedelta(days=31)
        date_to = datetime.today().date()
    elif "2023" == callback.data:
        return datetime.strptime("01.01.2023", "%d.%m.%Y").date(), \
            datetime.strptime("31.12.2023", "%d.%m.%Y").date()
    else:
        date_from = datetime.strptime(f'01.{callback.data}.{datetime.today().year}', "%d.%m.%Y").date()
        date_to = datetime.strptime(f'{monthrange(datetime.today().year, int(callback.data))[1]}.{callback.data}.'
                                    f'{datetime.today().year}', "%d.%m.%Y").date()
    return date_from, date_to


def __cut_big_output(string: str) -> str:
    return string[-3900::]