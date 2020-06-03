# A representation of database objects
class DiscountModel:
    id: int
    item: str
    min_quantity: int
    max_quantity: int  # This is added just if it is wanted to add a limit the amount of items that can be under a discount
    free_items: int = None
    discount_percentage: int = None
    type: str

    def __init__(
        self,
        id: int,
        item: str,
        min_quantity: int,
        max_quantity: int,
        type: str,
        free_items: int = None,
        discount_percentage: int = None,
    ):
        self.id = id
        self.item = item
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.type = type
        self.free_items = free_items
        self.discount_percentage = discount_percentage
