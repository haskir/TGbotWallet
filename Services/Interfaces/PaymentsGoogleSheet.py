from Services.Dataclasses import *
from Services.Interfaces import *
from datetime import datetime, date


class PaymentsGoogleSheet:
    @staticmethod
    def __date_sort(payment: Payment, start: str, stop: str) -> bool:
        def convert(d: str) -> datetime:
            return datetime.strptime(d, "%d.%m.%Y")

        return convert(start) <= convert(payment.transaction_date) <= convert(stop)

    @staticmethod
    def __total_sort(payment: Payment, start: int, stop: int) -> bool:
        # print(f"{payment=}\n{start=}\n{stop=}")
        return start <= payment.total <= stop

    @staticmethod
    def __category_sort(payment: Payment, start: str, stop=None) -> bool:
        # print(f"\n\n{payment=}\n{start=}\n{stop=}\n\n")
        return payment.category in start

    TOTALSORT = __total_sort
    DATESORT = __date_sort
    CATEGORYSORT = __category_sort

    def __init__(self, sheetHandler: GoogleSheets):
        self.sheetHandler = sheetHandler

    def show_all(self, sheet_uid: str) -> list[Payment] | None:
        index = self.sheetHandler.last_row(sheet_uid)
        return [Payment(*temp) for temp in self.sheetHandler.show_rows(sheet_uid,
                                                                       start=1,
                                                                       stop=index)]

    def write(self, sheet_uid: str, payment: Payment):
        index = self.sheetHandler.last_row(sheet_uid)
        response = self.sheetHandler.show_rows(sheet_uid,
                                               start=index,
                                               stop=index)
        if response is None:
            payment.uid = 1
        elif isinstance(response, list):
            payment.uid = int(response[0][0]) + 1
        self.sheetHandler.append_row(sheet_uid, list(payment))

    def delete_payment(self, sheet_id: str, payment_uid: str | int) -> bool:
        if isinstance(payment_uid, int):
            payment_uid = str(payment_uid)

        payments = self.show_all(sheet_id)
        if payments is None:
            return False
        try:
            for key, value in enumerate(pay.uid for pay in payments):
                # print(f"{payment_uid=}, {key=}, {value=}")
                if value == payment_uid:
                    print(key)
                    self.sheetHandler.delete_row(sheet_id, start=key, end=key + 1)
                    return True
        except IndexError:
            ...

    def sort(self, sheet_id: str, sort_type: callable, goal: tuple) -> list[Payment]:
        # print(f"{payments=}\n"
        #       f"{sort_type=}\n"
        #       f"{goal=}")
        return [pay for pay in self.show_all(sheet_id) if sort_type(pay, *goal)]

    @staticmethod
    def summa_payments(payments: list[Payment]) -> int | float:
        return sum([tran.total for tran in payments])


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    try:
        t_user.sheet_id = "1cbPYocbpmCPqLB-oQByNv1sv9aQHl5lNrjbruRfzF_A"
        t_pay = Payment(0, None, "Еда", "Пятёрочка", 999, "Чипсы")
        t_g_h = PaymentsGoogleSheet(s_handler)
        t_g_h.delete_payment(t_user.sheet_id, "7")
    except Exception as e:
        print(e)
    finally:
        input("Удалить таблицу")
        g_handler.delete_tests()
