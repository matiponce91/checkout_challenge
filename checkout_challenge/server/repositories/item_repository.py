from typing import List
from checkout_challenge.server.models import (
    ItemModel,
    ItemValueModel,
)


class ItemRepository:

    def get_all(self) -> List[ItemModel]:
        return [
            ItemModel(
                id=1,
                code='PEN',
                name='Lana Pen',
                value=[
                    ItemValueModel(id=1, price=500, currency='EUR')
                ]
            ),
            ItemModel(
                id=2,
                code='TSHIRT',
                name='Lana T-Shirt',
                value=[
                    ItemValueModel(id=2, price=2000, currency='EUR')
                ]
            ),
            ItemModel(
                id=3,
                code='MUG',
                name='Lana Coffee Mug',
                value=[
                    ItemValueModel(id=3, price=750, currency='EUR')
                ]
            ),
        ]
