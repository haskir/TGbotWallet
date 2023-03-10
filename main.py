from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from Services import *
from Interfaces import *

import os
import dotenv

dotenv.load_dotenv()

API_TOKEN: str = os.getenv('BOT_TOKEN')

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)

# Хендлеры для работы с гуглом и база юзеров
udb = UserDatabase()
googleHandler = GoogleDriver(path_to_ini="cred.ini")
sheetHandler = GoogleSheets(path_to_ini="cred.ini")
udb_g_sheet = UdbGoogleSheetHandler(googleHandler=googleHandler, sheetHandler=sheetHandler)
payments_handler = PaymentsGoogleSheet(sheetHandler=sheetHandler)
menu_keyboard = ReplyKeyboardBuilder()
default_keyboard = ReplyKeyboardBuilder()
check_keyboard = ReplyKeyboardBuilder()
googleHandler.delete_tests()
# Списки кнопок
check_button: list[KeyboardButton] = [KeyboardButton(text="Да")]

standart_buttons: list[KeyboardButton] = [KeyboardButton(text="Отмена"),
                                          KeyboardButton(text="Назад")]

menu_buttons: list[KeyboardButton] = [KeyboardButton(text="Новая покупка"),
                                      KeyboardButton(text="Новое пополнение"),
                                      KeyboardButton(text="Получить статистику"),
                                      KeyboardButton(text="Изменить e-mail")]


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user = message.from_user
    udb.add_user(User(uid=str(user.id),
                      is_bot=user.is_bot,
                      first_name=user.first_name,
                      last_name=user.last_name,
                      username=user.username,
                      language_code=user.language_code))
    await message.answer(text='Привет, этот бот - твой личный кошелёк\n\n'
                              'Чтобы начать нажми на /fillform')


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Ну давай сначала')
    user = udb.get_user(message.from_user.id)
    if user and user.email != "EMPTY_VALUE":
        await state.set_state(FSMewPayment.FSMMenuState)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего')


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text='Кто ты, воин?')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)


# Введено корректное имя
@dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    udb.get_user(str(message.from_user.id)).inner_name = message.text
    await message.answer(text='Спасибо!\n\nА теперь введите свой email для доступа к табличке')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_email)


# Введено Некорректное имя
@dp.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя')


# Если введен корректный email
@dp.message(StateFilter(FSMFillForm.fill_email), email_validation)
async def process_email_sent(message: Message, state: FSMContext):
    user = udb.get_user(message.from_user.id)
    user.email = message.text
    # user.sheet_id = googleHandler.create(user.username)
    await message.answer(text=f'Спасибо! Ссылка на табличку придёт вам на почту!')
    # user.sheet_id = googleHandler.create("test")
    # user.permission_id = googleHandler.create_permission(user.sheet_id, user.email)
    menu_keyboard.row(*menu_buttons)
    await message.answer(text="Что будем делать дальше?",
                         reply_markup=menu_keyboard.as_markup(),
                         resize_keyboard=True)
    await state.set_state(FSMewPayment.FSMMenuState)


# Введён Некорректный email
@dp.message(StateFilter(FSMFillForm.fill_email))
async def warning_not_email(message: Message):
    await message.answer(text='То, что вы отправили не похоже на корректный email\n\n')


@dp.message(StateFilter(FSMewPayment.FSMMenuState), Text(text="Новая покупка"))
async def new_payment(message: Message, state: FSMContext):
    await message.answer(text="Введите категорию траты",
                         reply_markup=ReplyKeyboardRemove())
    udb.get_user(message.from_user.id).state = {"Category": None,
                                                "Market": None,
                                                "Total": None,
                                                "Description": None}
    await state.set_state(FSMewPayment.FSMFillCategory)


@dp.message(StateFilter(FSMewPayment.FSMFillCategory), F.text.isalpha())
async def new_payment_category(message: Message, state: FSMContext):
    await message.answer(text="Введите название магазина")
    udb.get_user(message.from_user.id).state["Category"] = message.text
    await state.set_state(FSMewPayment.FSMFillMarket)


@dp.message(StateFilter(FSMewPayment.FSMFillMarket), F.text.isalpha())
async def new_payment_total(message: Message, state: FSMContext):
    await message.answer(text="Сколько потратили?")
    udb.get_user(message.from_user.id).state["Market"] = message.text
    await state.set_state(FSMewPayment.FSMFillTotal)


@dp.message(StateFilter(FSMewPayment.FSMFillTotal), F.text.isdigit())
async def new_payment_description(message: Message, state: FSMContext):
    await message.answer(text="Введите описание")
    udb.get_user(message.from_user.id).state["Total"] = message.text
    await state.set_state(FSMewPayment.FSMCheck)


@dp.message(StateFilter(FSMewPayment.FSMCheck))
async def new_payment_check(message: Message, state: FSMContext):
    udb.get_user(message.from_user.id).state["Description"] = message.text
    await message.answer(text=f"Всё верно?\n" + '\n'.join(udb.get_user(message.from_user.id).state.values()),
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMewPayment.FSMMenuState)


# БЕТА ФУНКЦИИ
@dp.message(StateFilter(FSMewPayment.FSMMenuState), Text(text="Новое пополнение"))
async def change_email(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")


@dp.message(StateFilter(FSMewPayment.FSMMenuState), Text(text="Получить статистику"))
async def get_statistic_menu(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")


@dp.message(StateFilter(FSMewPayment.FSMMenuState), Text(text="Изменить e-mail"))
async def get_statistic_menu(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")


@dp.message()
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')


if __name__ == '__main__':
    dp.run_polling(bot)
    ...
# Запускаем бота
