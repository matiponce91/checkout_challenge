from sys import exit
from typing import Any, Dict, List, Optional

from checkout_challenge.client.server_client import ServerClient


class Client:
    server_client: Any
    currency: str
    items: List[dict]
    discounts: List[dict]
    cart: dict

    def __init__(self, currency):
        self.server_client = ServerClient()
        self.currency = currency
        self.items = self.server_client.get_client('get_items').run_action()
        self.discounts = self.server_client.get_client('get_discounts').run_action()

    def is_valid_yes_or_no_option(self, option: str) -> bool:
        if option.lower() in ['no', 'n']:
            return False
        elif option.lower() in ['yes', 'y']:
            return True
        else:
            new_option = input('The value entered is invalid. Please try again')
            self.is_valid_yes_or_no_option(new_option)

    def is_valid_number_option(self, option: str, option_size: int = None) -> bool:
        try:
            option = int(option)
        finally:
            if type(option) == int and option_size is None:
                return True
            if type(option) == int and option <= option_size:
                return True
            elif type(option) == str and option.lower() == 'exit':
                exit()
            else:
                new_option = input(
                    'The value entered is invalid. Try again or if you want to exit, enter *exit*: '.format(
                        option_size,
                    ),
                )
                return self.is_valid_number_option(new_option, option_size)

    def add_item_to_cart(self):
        print('Which item do you want to add to your cart: \n')
        for item in self.items:
            print('{}- {} -> {} {}'.format(
                self.items.index(item) + 1,
                item['name'],
                item['value'][self.currency],
                self.currency,
            ))

        item_option: str = input('\nEnter desired option number:  ')
        if self.is_valid_number_option(item_option, len(self.items)):
            quantity = input('Enter how many *{}* do you want: '.format(self.items[int(item_option) - 1]['name']))
            if self.is_valid_number_option(quantity):
                self.cart[self.items[int(item_option) - 1]['code']] += int(quantity)

    def get_applicable_discounts(self) -> List[Optional[dict]]:
        applicable_discounts: List = []
        for key, value in self.cart.items():
            for discount in self.discounts:
                if discount['item'] == key:
                    # Check if minimum conditions is met
                    if value >= discount['min_quantity']:
                        applicable_discounts.append(discount)
        return applicable_discounts

    def get_item_by_code(self, code: str) -> Dict[str, str]:
        if code == 'PEN':
            return self.items[0]
        elif code == 'TSHIRT':
            return self.items[1]
        elif code == 'MUG':
            return self.items[2]

    def calculate_total(self,) -> int:
        amount: int = 0
        applicable_discounts: List[Optional[dict]] = self.get_applicable_discounts()
        for key, value in self.cart.items():
            if key == 'id':
                continue
            if value > 0:
                item = self.get_item_by_code(key)
                for discount in applicable_discounts:
                    if discount['type'] == 'FREE':
                        if discount['item'] == key:
                            quantity_to_discount: int = self.cart[discount['item']]
                            if discount['max_quantity'] > 0 and value > discount['max_quantity']['key']:
                                quantity_to_discount: int = discount['max_quantity']['key']

                            free_units: int = int(
                                self.cart[discount['item']] / discount['min_quantity']
                            )
                            amount += (quantity_to_discount-free_units) * item['value'][self.currency]
                            value -= quantity_to_discount

                    elif discount['type'] == 'BULK':
                        if discount['item'] == key:
                            quantity_to_discount: int = self.cart[discount['item']]
                            if discount['max_quantity'] > 0 and discount['max_quantity']['key'] < value:
                                quantity_to_discount: int = discount['max_quantity']['key']

                            amount += (
                                quantity_to_discount * item['value'][self.currency]
                            ) * (
                                1 - discount['discount_percentage'] / 100
                            )
                            value -= quantity_to_discount

                if value != 0:
                    amount += value * item['value'][self.currency]

        return amount

    def show_main_menu(self):
        print('Welcome to Lana store checkout')
        option = input('Do you want to start with checkout (Y/n): ')
        if self.is_valid_yes_or_no_option(option):
            self.cart = self.server_client.get_client('create_cart').run_action()
            amount: int = 0
            continue_with_checkout: bool = True
            while continue_with_checkout:
                self.add_item_to_cart()
                amount = self.calculate_total()
                option = input(
                    'Your cart total is {} {}. Do You want to continue adding items (Y/n): '.format(
                        amount / 100,
                        self.currency,
                    ),
                )
                if self.is_valid_yes_or_no_option(option) is False:
                    continue_with_checkout = False

            option = input('Your total is {} {}. Do you want to proceed (Y/n): '.format(amount / 100, self.currency))
            if self.is_valid_yes_or_no_option(option) is False:
                self.server_client.get_client('save_cart', cart=self.cart).run_action()
                exit()
        else:
            exit()


# if __name__ == '__main__':
#     client: Client = Client(currency='EUR')  # It would be assume that the selected currency is EUR
#     client.show_main_menu()
