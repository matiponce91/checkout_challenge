from checkout_challenge.server.actions import (
    CreateCartAction,
    GetItemsAction,
    GetDiscountsAction,
)
from typing import Any


class ServerClient:

    def get_client(self, action_to_call: str) -> Any:
        client = None
        if action_to_call == 'get_items':
            client = GetItemsAction()
        elif action_to_call == 'get_discounts':
            client = GetDiscountsAction()
        elif action_to_call == 'create_cart':
            client = CreateCartAction()

        return client
