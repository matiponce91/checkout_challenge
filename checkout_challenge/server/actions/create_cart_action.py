from checkout_challenge.server.services import CartService


class CreateCartAction:

    def run_action(self) -> dict:
        cart = CartService().create_cart()
        return {
            'id': cart.id,
            'PEN': cart.pen_quantity,
            'TSHIRT': cart.tshirt_quantity,
            'MUG': cart.mug_quantity,
        }
