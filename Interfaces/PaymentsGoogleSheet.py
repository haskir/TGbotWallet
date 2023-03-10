from Dataclasses import *
from Interfaces import *
from datetime import datetime, date


def _date_sort(payment: Payment, start: str, stop: str) -> bool:
    def convert(d: str) -> datetime:
        return datetime.strptime(d, "%d.%m.%Y")

    return convert(start) <= convert(payment.transaction_date) <= convert(stop)


def _total_sort(payment: Payment, start: str, stop: str) -> bool:
    total = int(payment.total)
    return int(start) <= total <= int(stop)


def _category_sort(payment: Payment, goal: list[str]) -> bool:
    return payment.category in goal


class PaymentsGoogleSheet:
    def __init__(self, sheetHandler: GoogleSheets):
        self.sheetHandler = sheetHandler

    def show_all(self, sheet_uid: str) -> list[list] | None:
        index = self.sheetHandler.last_row(sheet_uid)
        return self.sheetHandler.show_rows(sheet_uid,
                                           start=1,
                                           stop=index)

    def write(self, sheet_uid: str, payment: Payment, ):
        index = self.sheetHandler.last_row(sheet_uid)
        response = self.sheetHandler.show_rows(sheet_uid,
                                               start=index,
                                               stop=index)[0]
        if response is None:
            payment.uid = 1
        elif isinstance(response, list):
            payment.uid = int(response[0]) + 1
        self.sheetHandler.append_row(sheet_uid, list(payment))

    def sort(self, sheet_uid: str, sort_type: callable, goal) -> list:
        result = [Payment(*temp) for temp in self.show_all(sheet_uid)]
        return [tran for tran in result if sort_type(tran, goal)]

    def sort_category(self, sheet_uid, goal_category: list[str]) -> list:
        result = [Payment(*temp) for temp in self.show_all(sheet_uid)]
        return [payment for payment in result if _category_sort(payment, goal_category)]

    @staticmethod
    def summa_payments(payments: list[Payment]) -> int | float:
        return sum([tran.total for tran in payments])


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    try:
        t_user.sheet_id = g_handler.create("test")
        g_handler.create_permission(t_user.sheet_id, "haskird2@gmail.com")
        t_pay = Payment(0, "Еда", None, "Пятёрочка", 999, "Чипсы")
        t_g_h = PaymentsGoogleSheet(s_handler)
        t_g_h.write(t_user.sheet_id, t_pay)
        t_g_h.write(t_user.sheet_id, t_pay)
    except Exception as e:
        print(e)
    finally:
        input("Удалить таблицу")
        g_handler.delete_tests()
