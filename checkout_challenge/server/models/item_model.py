from typing import List


# A representation of database objects
class ItemValueModel:
    id: int
    amount: int
    currency: str

    def __init__(self, id: int, amount: int, currency: str):
        self.id = id
        self.amount = amount
        self.currency = currency


# A representation of database objects
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
