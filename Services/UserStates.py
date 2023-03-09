from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class FSMGRegistration(StatesGroup):
    FSMFillName = State()
    FSMFillEmail = State()


class FSMDefaultStateGroup(StatesGroup):
    FSMDefaultState = State()


class FSMewPayment(StatesGroup):
    FSMFillCategory = State()
    FSMFillMarket = State()
    FSMFillTotal = State()
    FSMFillDescription = State()


class FSMGetStatistic(StatesGroup):
    FSMGetByTotal = State()
    FSMGetByDate = State()
    FSMGETByCategory = State()
