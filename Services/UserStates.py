from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# Cоздаём класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    fill_name = State()  # Состояние ожидания ввода имени
    fill_email = State()  # Состояние ожидания ввода возраста


FSMMenuState = State()


class FSMewPayment(StatesGroup):
    FSMFillCategory = State()
    FSMFillMarket = State()
    FSMFillTotal = State()
    FSMFillDescription = State()
    FSMCheck = State()


class FSMGetStatistic(StatesGroup):
    FSMGetStatisticMenu = State()
    FSMGetAll = State()
    FSMGetByTotal = State()
    FSMGetByDate = State()
    FSMGetByCategory = State()
    FSMChoosingCategory = State()
    FSMDeletePaymentsByUid = State()


class FSMChangeSelf(StatesGroup):
    FSMChangeSelfMenu = State()
    FSMShowInfo = State()
    FSMChangeEmail = State()
    FSMChangeName = State()


class FSMEnrollment(StatesGroup):
    FSMCEnrollmentMenu = State()
    FSMEnrollmentShow = State()
    FSMEnrollmentNew = State()
    FSMCEnrollmentDelete = State()
