from aiogram.filters.state import State, StatesGroup


class FSM(State):
    def __init__(self):
        self.prev, self.next = None, None
        super().__init__()


FSMMenuState = FSM()


class FSMFillForm(StatesGroup):
    fill_name = FSM()
    fill_email = FSM()


class FSMewPayment(StatesGroup):
    FSMFillCategory = FSM()
    FSMFillMarket = FSM()
    FSMFillTotal = FSM()
    FSMFillDescription = FSM()
    FSMCheck = FSM()


class FSMGetStatistic(StatesGroup):
    FSMGetStatisticMenu = FSM()
    FSMGetAll = FSM()
    FSMGetByTotal = FSM()
    FSMGetByDate = FSM()
    FSMGetByCategory = FSM()
    FSMDeletePaymentsByUid = FSM()


class FSMChangeSelf(StatesGroup):
    FSMChangeSelfMenu = FSM()
    FSMShowInfo = FSM()
    FSMChangeEmail = FSM()
    FSMChangeName = FSM()


class FSMEnrollment(StatesGroup):
    FSMFillCategory = FSM()
    FSMFillTotal = FSM()
    FSMCheck = FSM()
