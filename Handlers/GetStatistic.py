from .imports import *


get_statistic_router: Router = Router()


@get_statistic_router.message(StateFilter(FSMMenuState), Text(text="Получить статистику"))
async def get_statistic_menu(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")
