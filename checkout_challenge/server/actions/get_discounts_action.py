from typing import List

from checkout_challenge.server.models import DiscountModel
from checkout_challenge.server.services import DiscountService


# The controller for this specific action a different possible option would be having one file with multiple
# related calls
class GetDiscountsAction:

    def run_action(self) -> List[dict]:
        discounts: List[DiscountModel] = DiscountService().get_all_discounts()
        discount_list: List[dict] = []
        for d in discounts:
            discount_list.append({
                'item': d.item,
                'base_quantity': d.base_quantity,
                'max_quantity': d.max_quantity,
                'free_items': d.free_items,
                'discount_percentage': d.discount_percentage,
                'type': d.type,
            })

        return discount_list
