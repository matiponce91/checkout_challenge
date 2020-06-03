from mock import patch

from checkout_challenge.client.main import Client


class TestClient:

    def test_is_valid_yes_or_no_option_with_n(self):
        result = Client(currency='EUR').is_valid_yes_or_no_option(option='n')

        assert result is False

    def test_is_valid_yes_or_no_option_with_no(self):
        result = Client(currency='EUR').is_valid_yes_or_no_option(option='no')

        assert result is False

    def test_is_valid_yes_or_no_option_with_y(self):
        result = Client(currency='EUR').is_valid_yes_or_no_option(option='y')

        assert result is True

    def test_is_valid_yes_or_no_option_with_yes(self):
        result = Client(currency='EUR').is_valid_yes_or_no_option(option='yes')

        assert result is True

    @patch('checkout_challenge.client.main.input')
    def test_is_valid_yes_or_no_option_with_wrong_option_and_then_false(self, input_mock):
        input_mock.return_value = 'no'

        Client(currency='EUR').is_valid_yes_or_no_option(option='wrong_parameter')

        assert input_mock.call_count == 1

    @patch('checkout_challenge.client.main.input')
    def test_is_valid_yes_or_no_option_with_wrong_option_and_then_true(self, input_mock):
        input_mock.return_value = 'yes'

        Client(currency='EUR').is_valid_yes_or_no_option(option='wrong_parameter')

        assert input_mock.call_count == 1

    def test_validate_numeric_option(self):
        result = Client(currency='EUR').validate_numeric_option(option='1')

        assert result == 1

    def test_validate_numeric_option_with_option_size(self):
        result = Client(currency='EUR').validate_numeric_option(option='2', option_size=2)

        assert result == 2

    @patch('checkout_challenge.client.main.input')
    def test_validate_numeric_option_with_invalid_option(self, input_mock):
        input_mock.return_value = '2'

        Client(currency='EUR').validate_numeric_option(option='invalid')

        assert input_mock.call_count == 1

    @patch('checkout_challenge.client.main.input')
    def test_validate_numeric_option_with_option_bigger_than_option_size(self, input_mock):
        input_mock.return_value = '2'

        Client(currency='EUR').validate_numeric_option(option='3', option_size=2)

        assert input_mock.call_count == 1

    def test_add_item_to_cart(self):
        item_code = 'ITEM_CODE'
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 100,
        }

        client.add_item_to_cart(item_code, 100)

        assert client.cart[item_code] == 200

    def test_remove_item_from_cart(self):
        item_code = 'ITEM_CODE'
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 100,
        }

        client.remove_item_from_cart(item_code, 100)

        assert client.cart[item_code] == 0

    def test_get_item_by_code(self):
        item_code = 'ITEM_CODE'
        items = [{
            'code': item_code,
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]
        client = Client(currency='EUR')
        client.items = items

        item = client.get_item_by_code(item_code)

        assert item['code'] == items[0]['code']
        assert item['name'] == items[0]['name']
        assert item['value'] == items[0]['value']

    def test_get_item_by_code_not_existing_code(self):
        items = [{
            'code': 'ITEM_CODE',
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]
        client = Client(currency='EUR')
        client.items = items

        item = client.get_item_by_code('NOT_EXISTING_CODE')

        assert item is None

    def test_get_applicable_discounts(self):
        discounts = [{
            'item': 'ITEM_CODE',
            'base_quantity': 1,
            'max_quantity': 2,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.discounts = discounts
        client.cart = {
            'ITEM_CODE': 100,
        }

        returned_discounts = client.get_applicable_discounts()

        assert len(returned_discounts) == 1
        assert returned_discounts[0]['item'] == discounts[0]['item']
        assert returned_discounts[0]['base_quantity'] == discounts[0]['base_quantity']
        assert returned_discounts[0]['max_quantity'] == discounts[0]['max_quantity']
        assert returned_discounts[0]['free_items'] == discounts[0]['free_items']
        assert returned_discounts[0]['type'] == discounts[0]['type']

    def test_get_applicable_discounts_with_not_existing_discount(self):
        discounts = [{
            'item': 'ITEM_CODE',
            'base_quantity': 1,
            'max_quantity': 2,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.discounts = discounts
        client.cart = {
            'ITEM_CODE_2': 100,
        }

        returned_discounts = client.get_applicable_discounts()

        assert len(returned_discounts) == 0

    def test_get_applicable_discounts_not_min_condition_reach(self):
        discounts = [{
            'item': 'ITEM_CODE',
            'base_quantity': 3,
            'max_quantity': 4,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.discounts = discounts
        client.cart = {
            'ITEM_CODE': 1,
        }

        returned_discounts = client.get_applicable_discounts()

        assert len(returned_discounts) == 0

    def test_get_applicable_discounts_multiple_discounts_returned(self):
        discounts = [{
            'item': 'ITEM_CODE_1',
            'base_quantity': 3,
            'max_quantity': 4,
            'free_items': 1,
            'type': 'FREE',
        }, {
            'item': 'ITEM_CODE_2',
            'base_quantity': 3,
            'max_quantity': 4,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.discounts = discounts
        client.cart = {
            'ITEM_CODE_1': 100,
            'ITEM_CODE_2': 100,
        }

        returned_discounts = client.get_applicable_discounts()

        assert len(returned_discounts) == 2
        assert returned_discounts[0]['item'] == discounts[0]['item']
        assert returned_discounts[0]['base_quantity'] == discounts[0]['base_quantity']
        assert returned_discounts[0]['max_quantity'] == discounts[0]['max_quantity']
        assert returned_discounts[0]['free_items'] == discounts[0]['free_items']
        assert returned_discounts[0]['type'] == discounts[0]['type']
        assert returned_discounts[1]['item'] == discounts[1]['item']
        assert returned_discounts[1]['base_quantity'] == discounts[1]['base_quantity']
        assert returned_discounts[1]['max_quantity'] == discounts[1]['max_quantity']
        assert returned_discounts[1]['free_items'] == discounts[1]['free_items']
        assert returned_discounts[1]['type'] == discounts[1]['type']

    def test_calculate_total(self):
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 5,
        }
        client.items = [{
            'code': 'ITEM_CODE',
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]

        response = client.calculate_total()

        assert response == 500

    @patch.object(Client, 'get_applicable_discounts')
    def test_calculate_total_with_discounts(self, client_mock):
        client_mock.return_value = [{
            'item': 'ITEM_CODE',
            'base_quantity': 2,
            'max_quantity': 100,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 5,
        }
        client.items = [{
            'code': 'ITEM_CODE',
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]

        response = client.calculate_total()

        assert response == 300

    @patch.object(Client, 'get_applicable_discounts')
    def test_calculate_total_with_discount_maximun_restriction_applied(self, client_mock):
        client_mock.return_value = [{
            'item': 'ITEM_CODE',
            'base_quantity': 2,
            'max_quantity': 2,
            'free_items': 1,
            'type': 'FREE',
        }]
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 5,
        }
        client.items = [{
            'code': 'ITEM_CODE',
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]

        response = client.calculate_total()

        assert response == 400

    def test_calculate_total_with_empty_cart(self):
        client = Client(currency='EUR')
        client.cart = {
            'ITEM_CODE': 0,
        }
        client.items = [{
            'code': 'ITEM_CODE',
            'name': 'item name',
            'value': {
                'EUR': 100,
            },
        }]

        response = client.calculate_total()

        assert response == 0
