from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


check_button: KeyboardButton = KeyboardButton(text="Да")

standart_buttons: list[KeyboardButton] = [KeyboardButton(text="Отмена"),
                                          KeyboardButton(text="Назад")]

menu_buttons: list[KeyboardButton] = [KeyboardButton(text="Новая покупка"),
                                      KeyboardButton(text="Новое пополнение"),
                                      KeyboardButton(text="Получить статистику"),
                                      KeyboardButton(text="Изменить e-mail")]


menu_keyboard = ReplyKeyboardBuilder()
default_keyboard = ReplyKeyboardBuilder()
check_keyboard = ReplyKeyboardBuilder()