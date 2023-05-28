from flask import *

from src.models import Login


class LoginController:

    def __init__(self, login: Login.LoginManagement):
        self.login_management = login

    def route(self):
        number = request.form.get("mobile_number")
        password = request.form.get("password")

        print(number)
        print(password)

        if not number or not password:
            return make_response(("no arguments provided", 403))


        return {result=str(self.login_management.login(number, password)),token='asd'}
