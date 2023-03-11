from .imports import *


change_self_router: Router = Router()


@change_self_router.message(StateFilter(FSMMenuState), Text(text="Изменить e-mail"))
async def get_statistic_menu(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")