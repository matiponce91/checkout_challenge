from checkout_challenge.server.repositories import ItemRepository
from checkout_challenge.server.models import ItemModel

from typing import List


class ItemService:

    def get_all_items(self) -> List[ItemModel]:
        return ItemRepository().get_all()
