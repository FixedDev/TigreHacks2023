import jwt
from flask import *

from src.models import Login
from src.models.Login import LoginResult


class LoginController:

    def __init__(self, login: Login.LoginManagement, config):
        self.login_management = login
        self.config = config

    def login(self):
        number = request.form.get("mobile_number")
        password = request.form.get("password")

        print(number)
        print(password)

        if not number or not password:
            return jsonify({"result": LoginResult.ERROR})

        result, user = self.login_management.login(number, password)

        if result == LoginResult.SUCCESS:
            token = jwt.encode({"id": str(user.id())},
                               key=self.config['SECRET_KEY'])
            return jsonify({"result": str(result), "token": token})

        return jsonify({"result": str(result)})
