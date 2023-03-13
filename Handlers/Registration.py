from .imports import *

registration_router: Router = Router()


@registration_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    user = message.from_user
    udb.add_user(User(uid=str(user.id),
                      is_bot=user.is_bot,
                      first_name=user.first_name,
                      last_name=user.last_name,
                      username=user.username,
                      language_code=user.language_code)
    )
    udb.get_user(message.from_user.id).state = {"Category": None,
                                                "Market": None,
                                                "Total": None,
                                                "Description": None}
    udb.get_user(message.from_user.id).inner_name = "tester"
    # await message.answer(text="Привет, этот бот - твой личный кошелёк\n\nЧтобы начать нажми на /fillform")
    [menu_keyboard.row(button) for button in menu_buttons if button not in menu_keyboard.buttons]
    await message.answer(text=f"Главное меню",
                         reply_markup=menu_keyboard.as_markup())
    await state.set_state(FSMMenuState)


# @registration_router.message(Command(commands='fillform'), StateFilter(default_state))
# async def process_fillform_command(message: Message, state: FSMContext):
#     await message.answer(text='Кто ты, воин?')
#     # Устанавливаем состояние ожидания ввода имени
#     await state.set_state(FSMFillForm.fill_name)
#
#
# # Введено корректное имя
# @registration_router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
# async def process_name_sent(message: Message, state: FSMContext):
#     udb.get_user(str(message.from_user.id)).inner_name = message.text
#     await message.answer(text='Спасибо!\n\nА теперь введите свой email для доступа к табличке')
#     # Устанавливаем состояние ожидания ввода возраста
#     await state.set_state(FSMFillForm.fill_email)
#
#
# # Введено Некорректное имя
# @registration_router.message(StateFilter(FSMFillForm.fill_name))
# async def warning_not_name(message: Message):
#     await message.answer(text='То, что вы отправили не похоже на имя\n\n'
#                               'Пожалуйста, введите ваше имя')
#
#
# # Если введен корректный email
# @registration_router.message(StateFilter(FSMFillForm.fill_email), email_validation)
# async def process_email_sent(message: Message, state: FSMContext):
#     user = udb.get_user(message.from_user.id)
#     user.email = message.text
#     # user.sheet_id = googleHandler.create(user.username)
#     await message.answer(text=f'Спасибо! Ссылка на табличку придёт вам на почту!')
#     # user.sheet_id = googleHandler.create("test")
#     # user.permission_id = googleHandler.create_permission(user.sheet_id, user.email)
#     menu_keyboard.row(*menu_buttons)
#     await message.answer(text="Что будем делать дальше?",
#                          reply_markup=menu_keyboard.as_markup(),
#                          resize_keyboard=True)
#     udb.get_user(message.from_user.id).state = {"Category": None,
#                                                 "Market": None,
#                                                 "Total": None,
#                                                 "Description": None}
#     await state.set_state(FSMMenuState)
#
#
# # Введён Некорректный email
# @registration_router.message(StateFilter(FSMFillForm.fill_email))
# async def warning_not_email(message: Message):
#     await message.answer(text='То, что вы отправили не похоже на корректный email\n\n')
