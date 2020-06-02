from typing import List

from checkout_challenge.server.models import ItemModel
from checkout_challenge.server.repositories import ItemRepository


class ItemService:

    def get_all_items(self) -> List[ItemModel]:
        return ItemRepository().get_all()
