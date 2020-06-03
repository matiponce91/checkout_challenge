from checkout_challenge.server.services import CartService


# The controller for this specific action a different possible option would be having one file with multiple
# related calls
class CreateVolatileCartAction:

    def run_action(self) -> dict:
        cart = CartService().create_cart()
        return {
            'id': cart.id,
            'PEN': cart.pen_quantity,
            'TSHIRT': cart.tshirt_quantity,
            'MUG': cart.mug_quantity,
        }
