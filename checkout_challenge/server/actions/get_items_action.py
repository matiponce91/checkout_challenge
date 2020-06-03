from typing import List

from checkout_challenge.server.models import ItemModel
from checkout_challenge.server.services import ItemService


# The controller for this specific action a different possible option would be having one file with multiple
# related calls
class GetItemsAction:

    def run_action(self) -> List[dict]:
        items: List[ItemModel] = ItemService().get_all_items()
        item_list: List[dict] = []
        for i in items:
            value = {}
            for price in i.values:
                value[price.currency] = price.amount

            item_list.append({
                'code': i.code,
                'name': i.name,
                'value': value,
            })

        return item_list
