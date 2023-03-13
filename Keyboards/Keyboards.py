from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton,
                                    InlineKeyboardBuilder, InlineKeyboardButton)
from aiogram.types import (KeyboardButton,
                           Message,
                           ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)


standart_buttons: list[KeyboardButton] = [
    KeyboardButton(text="Отмена"),
    KeyboardButton(text="Назад")
]

check_button: KeyboardButton = KeyboardButton(text="Да")

menu_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Новая покупка", callback_data="NewPayment"),
    InlineKeyboardButton(text="Новое пополнение", callback_data="NewEnrollment"),
    InlineKeyboardButton(text="Получить статистику", callback_data="GetStatistic"),
    InlineKeyboardButton(text="Профиль", callback_data="ChangeSelf"),
]

enrollment_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Показать историю", callback_data="EnrollmentShow"),
    InlineKeyboardButton(text="Новое пополнение", callback_data="EnrollmentNew"),
    InlineKeyboardButton(text="Удалить пополнение", callback_data="EnrollmentDelete"),
    InlineKeyboardButton(text="Назад", callback_data="BackToMainMenu"),
]

statistic_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="По датам", callback_data="StatisticByDate"),
    InlineKeyboardButton(text="По категории", callback_data="StatisticByCategory"),
    InlineKeyboardButton(text="По сумме", callback_data="StatisticByTotal"),
    InlineKeyboardButton(text="Назад", callback_data="BackToMainMenu"),
]

change_self_buttons: list[InlineKeyboardButton] = [
    InlineKeyboardButton(text="Информация", callback_data="ChangeSelfInfo"),
    InlineKeyboardButton(text="Изменить имя", callback_data="ChangeSelfName"),
    InlineKeyboardButton(text="Изменить адрес", callback_data="ChangeSelfEmail"),
    InlineKeyboardButton(text="Назад", callback_data="BackToMainMenu"),
]

menu_keyboard = InlineKeyboardBuilder()
statistic_keyboard = InlineKeyboardBuilder()
enrollment_keyboard = InlineKeyboardBuilder()
change_self_keyboard = InlineKeyboardBuilder()
default_keyboard = ReplyKeyboardBuilder()
check_keyboard = ReplyKeyboardBuilder()


default_keyboard.row(*standart_buttons)
[statistic_keyboard.add(button) for button in statistic_buttons]
[enrollment_keyboard.add(button) for button in enrollment_buttons]
change_self_keyboard.add(*change_self_buttons)
check_keyboard.add(*standart_buttons, check_button)
