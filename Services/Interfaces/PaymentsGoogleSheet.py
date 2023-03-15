from Services.Dataclasses import *
from Services.Interfaces import *
from datetime import datetime, date


def _date_sort(payment: Payment, start: str, stop: str) -> bool:
    def convert(d: str) -> datetime:
        return datetime.strptime(d, "%d.%m.%Y")

    return convert(start) <= convert(payment.transaction_date) <= convert(stop)


def _total_sort(payment: Payment, start: str, stop: str) -> bool:
    total = int(payment.total)
    return int(start) <= total <= int(stop)


def _category_sort(category: str, goal: list[str]) -> bool:
    return category in goal


class PaymentsGoogleSheet:
    def __init__(self, sheetHandler: GoogleSheets):
        self.sheetHandler = sheetHandler

    def show_all(self, sheet_uid: str) -> list[list] | None:
        index = self.sheetHandler.last_row(sheet_uid)
        return self.sheetHandler.show_rows(sheet_uid,
                                           start=1,
                                           stop=index)

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

        result = self.show_all(sheet_id)
        if result is None:
            return False
        try:
            for key, value in enumerate(row[0] for row in result):
                print(f"{payment_uid=}, {key=}, {value=}")
                if value == payment_uid:
                    print(key)
                    self.sheetHandler.delete_row(sheet_id, start=key, end=key+1)
                    return True
        except IndexError:
            ...

    def sort(self, sheet_uid: str, sort_type: callable, goal) -> list:
        result = [Payment(*temp) for temp in self.show_all(sheet_uid)]
        return [tran for tran in result if sort_type(tran, goal)]

    @staticmethod
    def sort_category(payments: list[list], goal_category: list[str] | str) -> list[list]:
        goal_category = [goal_category] if isinstance(goal_category, str) else goal_category
        return [payment for payment in payments if _category_sort(payment[2], goal_category)]

    @staticmethod
    def summa_payments(payments: list[Payment]) -> int | float:
        return sum([tran.total for tran in payments])


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    try:
        t_user.sheet_id = "1cbPYocbpmCPqLB-oQByNv1sv9aQHl5lNrjbruRfzF_A"
        t_pay = Payment(0, "Еда", None, "Пятёрочка", 999, "Чипсы")
        t_g_h = PaymentsGoogleSheet(s_handler)
        t_g_h.delete_payment(t_user.sheet_id, "7")
    except Exception as e:
        print(e)
    finally:
        input("Удалить таблицу")
        g_handler.delete_tests()

