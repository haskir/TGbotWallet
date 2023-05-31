import dataclasses
from datetime import date as date


@dataclasses.dataclass
class Enrollment:
    uid: int | None
    enrollment_date: str | None
    category: str
    total: int | float
    description: str

    def __post_init__(self):
        if self.enrollment_date is None:
            self.enrollment_date = date.today().strftime("%d.%m.%Y")
        self.total = int(self.total) if isinstance(self.total, str) else self.total

    def __iter__(self):
        return iter(list(self.__dict__.values()))

    def __next__(self):
        return next(iter(self))

    def __repr__(self):
        return "  ".join(str(value) for value in self.__dict__.values()) + "\n"

    def __str__(self):
        return f"{self.uid} {self.enrollment_date[:5:]} {self.total} {self.category} {self.description}\n"


