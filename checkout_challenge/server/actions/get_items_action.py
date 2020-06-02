from checkout_challenge.server.services import ItemService
from checkout_challenge.server.models import ItemModel
from typing import List


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
