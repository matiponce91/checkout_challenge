from checkout_challenge.server.repositories import CartRepository
from checkout_challenge.server.models import CartModel


class CartService:

    def create_cart(self) -> CartModel:
        return CartRepository().create()
