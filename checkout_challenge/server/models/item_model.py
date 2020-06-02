from typing import List


class ItemValueModel:
    id: int
    amount: int
    currency: str

    def __init__(self, id: int, amount: int, currency: str):
        self.id = id
        self.amount = amount
        self.currency = currency


class ItemModel:
    id: int
    code: str
    name: str
    values: List[ItemValueModel]

    def __init__(self, id: int, code: str, name: str, values: List[ItemValueModel]):
        self.id = id
        self.code = code
        self.name = name
        self.values = values
