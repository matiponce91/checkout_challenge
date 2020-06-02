class CartModel:
    id: int
    tshirt_quantity: int
    pen_quantity: int
    mug_quantity: int

    def __init__(self, id: int, tshirt_quantity: int, pen_quantity: int, mug_quantity: int):
        self.id = id
        self.tshirt_quantity = tshirt_quantity
        self.pen_quantity = pen_quantity
        self.mug_quantity = mug_quantity
