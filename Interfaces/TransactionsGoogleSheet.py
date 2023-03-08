from Dataclasses import *
from Interfaces import *


class TransactionsGoogleSheet:
    @classmethod
    def write(cls, sheet_uid: str, transaction: Transaction, sheethandler: GoogleSheets):
        transaction.uid = sheethandler.show(sheet_uid,
                                            start=sheethandler.last_row(sheet_uid),
                                            stop=sheethandler.last_row(sheet_uid) + 1)
        sheethandler.append_row(sheet_uid, list(transaction), category=transaction.category)


if __name__ == "__main__":
    t_user = User(1)
    g_handler = GoogleDriver()
    s_handler = GoogleSheets()
    uid_sheet = g_handler.create("test")
    g_handler.create_permission(uid_sheet, "haskird2@gmail.com")
    t_tran = Transaction(0, "Еда", None, "Пятёрочка", 999, "Чипсы")
    TransactionsGoogleSheet.write(uid_sheet, t_tran, s_handler)
    input("Удалить таблицу")
    g_handler.delete_tests()