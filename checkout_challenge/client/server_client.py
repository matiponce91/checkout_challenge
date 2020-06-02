from typing import Any

from checkout_challenge.server.actions import (CreateCartAction,
                                               GetDiscountsAction,
                                               GetItemsAction,
                                               SaveCartAction)


class ServerClient:

    def get_client(self, action_to_call: str, **kwargs) -> Any:
        client = None
        if action_to_call == 'get_items':
            client = GetItemsAction()
        elif action_to_call == 'get_discounts':
            client = GetDiscountsAction()
        elif action_to_call == 'create_cart':
            client = CreateCartAction(**kwargs)
        elif action_to_call == 'save_cart':
            client = SaveCartAction()

        return client
