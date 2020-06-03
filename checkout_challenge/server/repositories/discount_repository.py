from typing import List

from checkout_challenge.server.models import DiscountModel


# Here we can implement the ORM layer
class DiscountRepository:

    def get_all(self) -> List[DiscountModel]:
        return [
            DiscountModel(
                id=1,
                item='PEN',
                base_quantity=2,
                max_quantity=0,
                free_items=1,
                type='FREE'
            ),
            DiscountModel(
                id=2,
                item='TSHIRT',
                base_quantity=3,
                max_quantity=0,
                discount_percentage=25,
                type='BULK'
            ),
        ]
