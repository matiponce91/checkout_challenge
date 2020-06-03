class UpdateVolatileCartAction:

    cart: dict

    def __init__(self, **kwargs):
        self.cart = kwargs['cart']

    def run_action(self):
        pass
