import requests
from flask import Flask

from src.controllers.LoginController import LoginController
from src.models.Login import LoginManagement, hash_password
from src.models.db.DatabaseAccessController import MongoConnectionHandle, JsonConnectionData
from src.models.db.UserAccessObject import UserAccessObject

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test3'

with open("db.json", mode='r') as file_handle:
    connection_data = JsonConnectionData(file_handle)
    connection = MongoConnectionHandle(data=connection_data)
    user_access = UserAccessObject(connection.connection().get_database("dbtest").get_collection("users"))
    controller = LoginManagement(user_access, hash_password)

    var = LoginController(controller)

    app.add_url_rule("/internal_login", view_func=var.route, methods=["POST"])
    app.run(debug=True)