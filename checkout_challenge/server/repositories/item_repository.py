from typing import List

from checkout_challenge.server.models import ItemModel, ItemValueModel


class ItemRepository:

    def get_all(self) -> List[ItemModel]:
        return [
            ItemModel(
                id=1,
                code='PEN',
                name='Lana Pen',
                values=[ItemValueModel(id=1, amount=500, currency='EUR')]
            ),
            ItemModel(
                id=2,
                code='TSHIRT',
                name='Lana T-Shirt',
                values=[ItemValueModel(id=2, amount=2000, currency='EUR')]
            ),
            ItemModel(
                id=3,
                code='MUG',
                name='Lana Coffee Mug',
                values=[ItemValueModel(id=3, amount=750, currency='EUR')]
            ),
        ]
