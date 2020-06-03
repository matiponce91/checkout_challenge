from checkout_challenge.server.models import CartModel


# Here we can implement the ORM layer
class CartRepository:

    def create(self) -> CartModel:
        return CartModel(
            id=1,
            pen_quantity=0,
            tshirt_quantity=0,
            mug_quantity=0,
        )
