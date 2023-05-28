from flask import Flask

from src.controllers.LoginController import LoginController
from src.controllers.SignupController import SignupController
from src.models.Login import LoginManagement, hash_password
from src.models.SignUp import SignupHandler
from src.models.db.DatabaseAccessController import MongoConnectionHandle, JsonConnectionData
from src.models.db.UserAccessObject import UserAccessObject

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test3'

with open("db.json", mode='r') as file_handle:
    connection_data = JsonConnectionData(file_handle)
    connection = MongoConnectionHandle(data=connection_data)
    user_access = UserAccessObject(connection.connection().get_database("dbtest").get_collection("users"))
    login_controller = LoginManagement(user_access, hash_password)
    signup_controller = SignupHandler(user_access, hash_password)

    login = LoginController(login_controller, app.config)
    signup = SignupController(signup_controller, app.config)

    app.add_url_rule("/internal_login", view_func=login.login, methods=["POST", "OPTION"])
    app.add_url_rule("/internal_register", view_func=signup.signup, methods=["POST", "OPTION"])

    app.run(debug=True)
