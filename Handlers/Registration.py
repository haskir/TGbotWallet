from .imports import *

registration_router: Router = Router()


@registration_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    user = message.from_user
    if udb_g_sheet.user_already_in_google_db(user.id):
        udb.get_user()
    udb.add_user(User(uid=str(user.id),
                      inner_name="",
                      first_name=user.first_name,
                      last_name=user.last_name,
                      username=user.username,
                      language_code=user.language_code,
                      email="",
                      sheet_id="",
                      permission_id="",
                      state={"Category": None,
                             "Market": None,
                             "Total": None,
                             "Description": None}
                      )
                 )
    await message.answer(text="Привет, этот бот - твой личный кошелёк\nЧтобы начать введи своё имя")


# Введено корректное имя
@registration_router.message(StateFilter(default_state), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    udb.get_user(str(message.from_user.id)).inner_name = message.text
    await message.answer(text='Спасибо!\n\nА теперь введите свой email для доступа к табличке')
    # Устанавливаем состояние ожидания ввода возраста
    await state.set_state(FSMFillForm.fill_email)


# Введено Некорректное имя
@registration_router.message(StateFilter(default_state))
async def warning_not_name(message: Message):
    await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                              'Пожалуйста, введите ваше имя')


# Если введен корректный email
@registration_router.message(StateFilter(FSMFillForm.fill_email), email_validation)
async def process_email_sent(message: Message, state: FSMContext):
    user = udb.get_user(message.from_user.id)
    print(user)
    udb_g_sheet.upload_database_to_google(user)
    user.email = message.text
    if not udb_g_sheet.user_already_in_google_db(user):
        user.sheet_id = googleHandler.create(user.username)
        user.permission_id = googleHandler.create_permission(user.sheet_id, user.email)
        udb_g_sheet
        await message.answer(text=f'Спасибо! Ссылка на табличку придёт вам на почту!',
                             reply_markup=menu_keyboard.as_markup(),
                             resize_keyboard=True)
    else:
        await message.answer(text=f'О, я вас знаю, вы у нас уже были!\n'
                                  f'Вот, что я умею:\n',
                             reply_markup=menu_keyboard.as_markup(),
                             resize_keyboard=True)
    await state.set_state(FSMMenuState)


# Введён Некорректный email
@registration_router.message(StateFilter(FSMFillForm.fill_email))
async def warning_not_email(message: Message):
    await message.answer(text='То, что вы отправили не похоже на корректный email\n\n')
