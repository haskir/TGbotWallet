from .imports import *


new_enrollment_router: Router = Router()


@new_enrollment_router.message(StateFilter(FSMMenuState), Text(text="Новое пополнение"))
async def new_enrollment(message: Message, state: FSMContext):
    await message.reply("Извини, это пока ещё недопилено")