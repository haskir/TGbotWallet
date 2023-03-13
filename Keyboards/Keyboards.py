from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton,
                                    InlineKeyboardBuilder, InlineKeyboardButton)
from aiogram.types import (KeyboardButton,
                           Message,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

check_button: KeyboardButton = KeyboardButton(text="Да")

standart_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Отмена", callback_data="Cancel"),
    InlineKeyboardButton(text="Назад", callback_data="Back")
]

menu_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Новая покупка", callback_data="NewPayment"),
    InlineKeyboardButton(text="Новое пополнение", callback_data="NewEnrollment"),
    InlineKeyboardButton(text="Получить статистику", callback_data="GetStatistic"),
    InlineKeyboardButton(text="Изменить e-mail", callback_data="ChangeSelf")
]

menu_keyboard = InlineKeyboardBuilder()
default_keyboard = InlineKeyboardBuilder()
check_keyboard = ReplyKeyboardBuilder()
