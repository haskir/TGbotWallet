import dataclasses
from datetime import date as date


@dataclasses.dataclass
class Payment:
    uid: int | None
    transaction_date: str | None
    category: str
    market: str
    total: int | float
    description: str

    def __post_init__(self):
        if self.transaction_date is None:
            self.transaction_date = date.today().strftime("%d.%m.%Y")

    def __iter__(self):
        return iter(list(self.__dict__.values()))

    def __next__(self):
        return next(iter(self))

    def __repr__(self):
        return "Transaction - " + " ".join(str(value) for value in self.__dict__.values())


if __name__ == "__main__":
    t_tran = Payment(1, None, "Еда", "Пятёрочка", 999, "Чипсы")
    print(list(t_tran))
    print(t_tran)