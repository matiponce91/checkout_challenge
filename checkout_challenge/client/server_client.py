from typing import Any

from checkout_challenge.server.actions import (
    CreateVolatileCartAction,
    GetDiscountsAction,
    GetItemsAction,
    SaveCartAction,
    UpdateVolatileCartAction,
)


# This is a mock of a potential client that could be HTTP or through any other transport
class ServerClient:

    def get_client(self, action_to_call: str, **kwargs) -> Any:
        client = None
        if action_to_call == 'get_items':
            client = GetItemsAction()
        elif action_to_call == 'get_discounts':
            client = GetDiscountsAction()
        elif action_to_call == 'create_volatile_cart':
            client = CreateVolatileCartAction()
        elif action_to_call == 'save_cart':
            client = SaveCartAction(**kwargs)
        elif action_to_call == 'update_volatile_cart':
            client = UpdateVolatileCartAction(**kwargs)

        return client
