from checkout_challenge.server.services import DiscountService
from checkout_challenge.server.models import DiscountModel
from typing import List


class GetDiscountsAction:

    def run_action(self) -> List[dict]:
        discounts: List[DiscountModel] = DiscountService().get_all_discounts()
        discount_list: List[dict] = []
        for d in discounts:
            discount_list.append({
                'item': d.item,
                'min_quantity': d.min_quantity,
                'max_quantity': d.max_quantity,
                'free_items': d.free_items,
                'type': d.type,
            })

        return discount_list
