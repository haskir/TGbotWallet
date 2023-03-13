from .imports import *

menu_router: Router = Router()

states = {
    "NewPayment": [FSMewPayment.FSMFillCategory, "Введите категорию траты"],
    "NewEnrollment": [FSMNewEnrollment, "Это ещё не допилено"],
    "GetStatistic": [FSMGetStatistic, "Это ещё не допилено"],
    "ChangeSelf": [FSMChangeSelf, "Это ещё не допилено"]
}
default_keyboard.row(*standart_buttons)


@menu_router.callback_query(StateFilter(FSMMenuState))
async def go_from_menu_to(callback: CallbackQuery, state: FSMContext):
    if callback.data in states.keys():
        await state.set_state(states.get(callback.data)[0])
        await callback.answer(states.get(callback.data)[1])


@menu_router.message(Command(commands='cancel'), StateFilter(default_state, FSMMenuState))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего')


@menu_router.message(Command(commands='cancel'), ~StateFilter(FSMMenuState))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Ну давай сначала')
    user = udb.get_user(message.from_user.id)
    if user and user.email != "EMPTY_VALUE":
        await state.set_state(FSMMenuState)
