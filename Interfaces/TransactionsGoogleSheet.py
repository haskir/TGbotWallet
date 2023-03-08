from Dataclasses import *
from Interfaces import *


class TransactionsGoogleSheet:
    @classmethod
    def write(cls, db_uid: str, transaction: Transaction, sheethandler: GoogleSheets):
        sheethandler.append_row(db_uid, list(transaction))


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    uid_sheet = g_handler.create("test")
    g_handler.create_permission(uid_sheet, "haskird2@gmail.com")
    t_tran = Transaction(1, "Еда", None, "Пятёрочка", 999, "Чипсы")
    TransactionsGoogleSheet.write(uid_sheet, t_tran, s_handler)
    input("Удалить таблицу")
    g_handler.delete_tests()