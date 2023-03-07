from dataclasses import dataclass
from datetime import date as date


@dataclass
class Transaction:
    uid: int
    transaction_date: date
    market: str
    category: str
    total: int | float
    description: str


if __name__ == "__main__":
    today = date.today()
    print(today)