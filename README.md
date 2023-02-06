## PIZZA DELIVERY API
This is a REST API for a Pizza delivery


## ROUTES TO IMPLEMENT
| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/auth/signup/``` | _Register new user_| _All users_|
| *POST* | ```/auth/login/``` | _Login user_|_All users_|
| *POST* | ```/auth/refresh/``` | _Refresh user token_|_All users_|
| *POST* | ```/orders``` | _Place an order_|_All users_|
| *PUT* | ```/orders/update/{order_id}/``` | _Update an order_|_All users_|
| *DELETE* | ```/orders/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/orders/get_info/``` | _Get user's orders_|_All users_|
| *GET* | ```/orders/get_list/``` | _List all orders made_|_Superuser_|
| *GET* | ```/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/orders/get_info/{order_id}/``` | _Get user's specific order_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|

## How to run the Project
- Install Postgreql
- Install Python
- Git clone the project with ``` git clone https://github.com/jetigenov/order_fastapi```
- Create your virtualenv with `Pipenv` or `virtualenv` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```
- Set Up your PostgreSQL database and set its URI in your ```database.py```
```
engine=create_engine('postgresql://postgres:<username>:<password>@localhost/<db_name>',
    echo=True
)
```

- Create your database by running ``` python init_db.py ```
- Finally run the API
``` uvicorn main:app ``
