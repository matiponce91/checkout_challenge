# The controller for this specific action a different possible option would be having one file with multiple
# related calls
class SaveCartAction:

    cart: dict

    def __init__(self, **kwargs):
        self.cart = kwargs['cart']

    def run_action(self):
        print('Cart {} saved successfully'.format(self.cart['id']))