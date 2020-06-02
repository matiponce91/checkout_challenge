class SaveCartAction:

    cart: dict

    def __init__(self, **kwargs):
        self.cart = kwargs['cart']

    def run_action(self):
        print('Cart {} saved successfully'.format(self.cart['id']))