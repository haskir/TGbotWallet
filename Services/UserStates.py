from aiogram.filters.state import State, StatesGroup


class FSM(State):
    def __init__(self):
        self.prev, self.next = None, None
        super().__init__()


FSMMenuState = FSM()


class FSMFillForm(StatesGroup):
    fill_name = FSM()
    fill_email = FSM()

    fill_name.next, fill_email.prev = fill_email, fill_name
    fill_name.prev = FSMMenuState


class FSMewPayment(StatesGroup):
    FSMFillCategory = FSM()
    FSMFillMarket = FSM()
    FSMFillTotal = FSM()
    FSMFillDescription = FSM()
    FSMCheck = FSM()

    FSMFillCategory.prev, FSMFillCategory.next = FSMMenuState, FSMFillMarket
    FSMFillMarket.prev, FSMFillMarket.next = FSMFillCategory, FSMFillTotal
    FSMFillTotal.prev, FSMFillTotal.next = FSMFillMarket, FSMFillDescription
    FSMFillDescription.prev, FSMFillDescription.next = FSMFillTotal, FSMCheck
    FSMCheck.prev, FSMCheck.next = FSMFillDescription, FSMMenuState


class FSMGetStatistic(StatesGroup):
    FSMGetStatisticMenu = FSM()
    FSMGetAll = FSM()
    FSMGetByTotal = FSM()
    FSMGetByDate = FSM()
    FSMGetByCategory = FSM()
    FSMDeletePaymentsByUid = FSM()

    FSMGetStatisticMenu.prev = FSMMenuState
    FSMGetByDate.prev = FSMGetStatisticMenu
    FSMGetByCategory.prev = FSMGetStatisticMenu
    FSMGetByCategory.prev,  FSMGetByCategory.next = FSMGetStatisticMenu, FSMGetStatisticMenu
    FSMDeletePaymentsByUid.prev, FSMDeletePaymentsByUid.next = FSMGetStatisticMenu, FSMGetStatisticMenu


class FSMChangeSelf(StatesGroup):
    FSMChangeSelfMenu = FSM()
    FSMShowInfo = FSM()
    FSMChangeEmail = FSM()
    FSMChangeName = FSM()

    FSMChangeSelfMenu.prev = FSMMenuState
    FSMShowInfo.prev = FSMMenuState
    FSMChangeEmail.prev, FSMChangeName.prev = FSMChangeSelfMenu, FSMChangeSelfMenu


class FSMEnrollment(StatesGroup):
    FSMCEnrollmentMenu = FSM()
    FSMEnrollmentShow = FSM()
    FSMEnrollmentNew = FSM()
    FSMCEnrollmentDelete = FSM()

    FSMCEnrollmentMenu.prev = FSMMenuState
    FSMEnrollmentNew.prev = FSMEnrollmentNew
    FSMCEnrollmentDelete.prev = FSMEnrollmentNew
