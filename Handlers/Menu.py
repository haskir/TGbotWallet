from .imports import *


menu_router: Router = Router()


@menu_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего')


@menu_router.message(Command(commands='cancel'), StateFilter(FSMMenuState))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего')


@menu_router.message(Command(commands='cancel'), ~StateFilter(FSMMenuState))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Ну давай сначала')
    user = udb.get_user(message.from_user.id)
    if user and user.email != "EMPTY_VALUE":
        await state.set_state(FSMMenuState)