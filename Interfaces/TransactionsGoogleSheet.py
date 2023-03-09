from Dataclasses import *
from Interfaces import *
from datetime import datetime, date


def _date_sort(transaction: Transaction, start: str, stop: str) -> bool:
    def convert(d: str) -> datetime:
        return datetime.strptime(d, "%d.%m.%Y")

    return convert(start) <= convert(transaction.transaction_date) <= convert(stop)


def _total_sort(transaction: Transaction, start: str, stop: str) -> bool:
    total = int(transaction.total)
    return int(start) <= total <= int(stop)


def _category_sort(transaction: Transaction,  goal: list[str]) -> bool:
    return transaction.category in goal


class TransactionsGoogleSheet:
    def __init__(self, sheethandler: GoogleSheets):
        self.sheethandler = sheethandler

    def show_all(self, sheet_uid: str) -> list[list] | None:
        index = self.sheethandler.last_row(sheet_uid)
        return self.sheethandler.show_rows(sheet_uid,
                                           start=1,
                                           stop=index)

    def write(self, sheet_uid: str, transaction: Transaction, ):
        index = self.sheethandler.last_row(sheet_uid)
        response = self.sheethandler.show_rows(sheet_uid,
                                               start=index,
                                               stop=index)[0]
        if response is None:
            transaction.uid = 1
        elif isinstance(response, list):
            transaction.uid = int(response[0]) + 1
        self.sheethandler.append_row(sheet_uid, list(transaction))

    def sort(self, sheet_uid: str, sort_type: callable, goal) -> list:
        result = [Transaction(*temp) for temp in self.show_all(sheet_uid)]
        return [tran for tran in result if sort_type(tran, goal)]

    def sort_category(self, sheet_uid, goal_category: list[str]) -> list:
        result = [Transaction(*temp) for temp in self.show_all(sheet_uid)]
        return [tran for tran in result if _category_sort(tran, goal_category)]


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    try:
        t_user.sheet_id = g_handler.create("test")
        g_handler.create_permission(t_user.sheet_id, "haskird2@gmail.com")
        t_tran = Transaction(0, "Еда", None, "Пятёрочка", 999, "Чипсы")
        t_g_h = TransactionsGoogleSheet(s_handler)
        t_g_h.write(t_user.sheet_id, t_tran)
        t_g_h.write(t_user.sheet_id, t_tran)
    except Exception as e:
        print(e)
    finally:
        input("Удалить таблицу")
        g_handler.delete_tests()
