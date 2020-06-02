from typing import List

from checkout_challenge.server.models import DiscountModel
from checkout_challenge.server.repositories import DiscountRepository


class DiscountService:

    def get_all_discounts(self) -> List[DiscountModel]:
        return DiscountRepository().get_all()
