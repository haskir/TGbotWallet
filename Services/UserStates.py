from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class FSMGRegistration(StatesGroup):
    FSMFillName = State()


class FSMGNewPayment(StatesGroup):
    ...