from checkout_challenge.server.models import CartModel


class CartRepository:

    def create(self) -> CartModel:
        return CartModel(
            id=1,
            pen_quantity=0,
            tshirt_quantity=0,
            mug_quantity=0,
        )
