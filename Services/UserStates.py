from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# Cоздаём класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    fill_name = State()  # Состояние ожидания ввода имени
    fill_email = State()  # Состояние ожидания ввода возраста


class FSMewPayment(StatesGroup):
    FSMMenuState = State()
    FSMFillCategory = State()
    FSMFillMarket = State()
    FSMFillTotal = State()
    FSMFillDescription = State()


class FSMGetStatistic(StatesGroup):
    FSMGetByTotal = State()
    FSMGetByDate = State()
    FSMGETByCategory = State()


class FSMChangeEmail(StatesGroup):
    ...
