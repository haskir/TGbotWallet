import dataclasses
from datetime import date as date


@dataclasses.dataclass
class Transaction:
    uid: int | None
    category: str
    transaction_date: str | None
    market: str
    total: int | float
    description: str

    def __post_init__(self):
        if self.transaction_date is None:
            self.transaction_date = date.today().strftime("%d.%m.%Y")

    def __iter__(self):
        return iter([value for key, value in self.__dict__.items() if key != "category"])

    def __next__(self):
        return next(iter(self))


if __name__ == "__main__":
    t_tran = Transaction(1, "Еда", None, "Пятёрочка", 999, "Чипсы")
    print(list(t_tran))