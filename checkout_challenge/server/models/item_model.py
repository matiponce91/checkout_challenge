from typing import List


class ItemValueModel:
    amount: str
    currency: int


class ItemModel:
    id: int
    code: str
    name: str
    values: List[ItemValueModel]
