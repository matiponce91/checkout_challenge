import os
os.getcwd()
import ipdb;ipdb.set_trace()
from checkout_challenge.client.main import Client


if __name__ == '__main__':
    client: Client = Client(currency='EUR')  # It would be assume that the selected currency is EUR
    client.show_main_menu()
