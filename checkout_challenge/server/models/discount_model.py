class DiscountModel:
    id: int
    item: str
    min_quantity: int
    max_quantity: int  # This is added just if it is wanted to add a limit the amount of items that can be under a discount
    free_items: int = None
    type: str
