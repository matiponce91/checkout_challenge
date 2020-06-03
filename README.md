# CHECKOUT CHALLENGE

## Project structure
The project is divided in two parts:
1- Client side
2- Server side

The first one (under `client` folder) is just a console client that calls the server side through a client (this `client` calls directly to
server code but it is though to allow implement any king of transport layer)

The second one (under `server` folder) is the server code. Its structure is the following:
* actions: all the endpoints that the server allows. There is one class per actions so also could an option to have one
class with all the related endpoints (for example: having under class `Discount` all the endpoints to 
get/create/delete/update discounts instead of having 4 different classes). Actions are in charge of receiving request
data, call the appropriate service and build the response.
* services: here is where the logic is contained. Services are in charge of communicating with different layers, doing
code logic and get all the needed information.
* repository: this is the ORM layer, potentially in charge of doing database SELECTS/INSERTS/DELETES/UPDATES
* models: the database object representations.