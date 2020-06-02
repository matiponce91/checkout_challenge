from checkout_challenge.server.repositories import DiscountRepository
from checkout_challenge.server.models import DiscountModel

from typing import List


class DiscountService:

    def get_all_discounts(self) -> List[DiscountModel]:
        return DiscountRepository().get_all()
