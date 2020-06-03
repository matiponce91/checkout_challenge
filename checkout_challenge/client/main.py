from os import system
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

    def validate_numeric_option(self, option: str, option_size: int = None) -> int:
        try:
            option = int(option)
        finally:
            if type(option) == int and option_size is None:
                return option
            if type(option) == int and option <= option_size:
                return option
            else:
                new_option = input('The value entered is invalid. Try again: ')
                return self.validate_numeric_option(new_option, option_size)

    def add_item_to_cart(self):
        print('Which item do you want to add at your shopping cart: \n')
        for item in self.items:
            print('{}- {} -> {} {}'.format(
                self.items.index(item) + 1,
                item['name'],
                item['value'][self.currency],
                self.currency,
            ))

        item_option: str = input('\nEnter desired option number:  ')
        validated_option: int = self.validate_numeric_option(item_option, len(self.items))

        quantity: str = input('Enter how many *{}* do you want: '.format(self.items[validated_option - 1]['name']))
        validated_quantity: int = self.validate_numeric_option(quantity)

        self.cart[self.items[validated_option - 1]['code']] += validated_quantity
        # Update the volatile cart information contained on server side.
        self.server_client.get_client('update_volatile_cart', cart=self.cart).run_action()

    def remove_item_from_cart(self):
        index: int = 0
        option_index: dict = {}
        message: str = ''
        for item in self.items:
            if self.cart[item['code']] > 0:
                option_index[index] = item
                message += '{}- {} -> currently {}\n'.format(
                    index + 1,
                    item['name'],
                    self.cart[item['code']],
                )
                index += 1

        if not option_index:
            input('Shopping cart is empty. Press any key to return to main menu.')
        else:
            print('Which item do you want to remove from your shopping cart: \n')
            print(message)
            item_option: str = input('Enter desired option number:  ')
            validated_option: int = self.validate_numeric_option(item_option, index)

            quantity: str = input('Enter how many *{}* do you want to remove (currently: {}): '.format(
                option_index[validated_option - 1]['name'],
                self.cart[option_index[validated_option - 1]['code']],
            ))
            validated_quantity: int = self.validate_numeric_option(
                quantity,
                self.cart[option_index[validated_option - 1]['code']],
            )

            self.cart[option_index[validated_option - 1]['code']] -= validated_quantity
            # Update the volatile cart information contained on server side.
            self.server_client.get_client('update_volatile_cart', cart=self.cart).run_action()

    def get_applicable_discounts(self) -> List[Optional[dict]]:
        """
        This function checks, based on the amount of items in cart, which discounts can be applied

        """
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
        """
        It is better to implement this calculation on the client side just to avoid having to call the server just
        to get the total. This is mainly because as this function will be called every time the user add a new
        item so that multiplies for all the users adding items, could add huge load to the server

        """
        amount: int = 0
        applicable_discounts: List[Optional[dict]] = self.get_applicable_discounts()
        for key, value in self.cart.items():
            if key == 'id':
                continue
            if value > 0:
                item = self.get_item_by_code(key)
                for discount in applicable_discounts:
                    # I have thought in two different kind of discounts: the buy X get Y free where it is represented
                    # here with the type `FREE` and they have a property `free_units`. That property tell us how many
                    # items the client would get for free.
                    # The other type is BULK and this time the property used is called `discount_percentage`.
                    # In a database both discounts would be saved in the same table but each one would have the other
                    # property as NULL
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
        option: str = input('Do you want to start with checkout (Y/n): ')
        if self.is_valid_yes_or_no_option(option):
            # With this we create a volatile cart, what means that this is not saved in the common database just to
            # avoid saving trash in the database if the user doesn't want to buy anything. Meanwhile the transaction
            # is not finished it can be store in for a Redis or any kind of volatile database
            self.cart = self.server_client.get_client('create_volatile_cart').run_action()
            amount: int = 0
            continue_with_checkout: bool = True
            while continue_with_checkout:
                system('clear')
                print('Your shopping cart total is {} {}. Do You want to: \n'.format(amount / 100, self.currency))
                print('1- Add more items to your cart')
                print('2- Remove an item from cart')
                print('3- Finalize purchase')
                print('4- Exit')
                option = input('\nEnter desired option number: ')
                validated_option: int = self.validate_numeric_option(option, 4)
                if validated_option == 1:
                    system('clear')
                    self.add_item_to_cart()
                elif validated_option == 2:
                    system('clear')
                    self.remove_item_from_cart()
                elif validated_option == 3:
                    system('clear')
                    continue_with_checkout = False
                else:
                    system('clear')
                    exit()
                # Each time cart content is modified (items are added/removed), the total amount is updated and shown
                # to the user
                amount = self.calculate_total()

            option = input('Your total is {} {}. Do you want to proceed (Y/n): '.format(amount / 100, self.currency))
            if self.is_valid_yes_or_no_option(option) is True:
                self.server_client.get_client('save_cart', cart=self.cart).run_action()

            exit()
        else:
            exit()


# if __name__ == '__main__':
#     client: Client = Client(currency='EUR')  # It would be assume that the selected currency is EUR
#     client.show_main_menu()
