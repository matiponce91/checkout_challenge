from checkout_challenge.server.models import CartModel
from checkout_challenge.server.repositories import CartRepository


class CartService:

    def create_cart(self) -> CartModel:
        return CartRepository().create()
