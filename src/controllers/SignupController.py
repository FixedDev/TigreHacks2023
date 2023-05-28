import jwt
from flask import *

from src.models import Login, SignUp
from src.models.Login import LoginResult
from src.models.SignUp import RegisterResult


class SignupController:

    def __init__(self, signup: SignUp.SignupHandler, config):
        self.signup_management = signup
        self.config = config

    def signup(self):
        number = request.form.get("mobile_number")
        password = request.form.get("password")

        print(number)
        print(password)

        if not number or not password:
            return jsonify({"result": RegisterResult.ERROR})

        result, user = self.signup_management.registerUser(number, password)

        if result == RegisterResult.SUCCESS:
            token = jwt.encode({"id": str(user.id())},
                               key=self.config['SECRET_KEY'])
            return jsonify({"result": str(result), "token": token})

        return jsonify({"result": str(result)})
