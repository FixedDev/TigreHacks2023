import logging
from enum import Enum

import pymongo
from bcrypt import *

from src.controllers.db.DatabaseAccessController import MongoConnectionHandle, JsonConnectionData
from src.models.User import User


class LoginResult(Enum):
    SUCCESS = 1,
    WRONG_PASSWORD = 2,
    USER_NOT_EXISTS = 3,
    ERROR = 4


def checkIfValid(password, user):
    return checkpw(password, user.passwd_hash)


def hash_password(password):
    salt = gensalt()
    hashed_passwd = hashpw(password, salt)

    return salt, hashed_passwd


class LoginController:
    def __init__(self, db_access_object: pymongo.collection, password_hash_algor):
        self.db_access_object = db_access_object
        self.password_hash_algor = password_hash_algor

    def user_exists(self, mobile_number):
        return self.db_access_object.find_one(
            filter={"mobile_number": mobile_number}
        ) is not None

    def login(self, mobile_number, password) -> LoginResult:
        try:
            document = self.db_access_object.find_one(filter={"mobile_number": mobile_number})

            if document is None:
                return LoginResult.USER_NOT_EXISTS

            user = User(document)

            return LoginResult.SUCCESS if checkIfValid(password, user) else LoginResult.WRONG_PASSWORD
        except Exception as e:
            logging.exception(e)
            return LoginResult.ERROR

    # db_access_object.search({name: user_name}).then(__check_if_valid)
    # si es valido, devolver un SUCCESS, si el usuario no se encuentra, INVALID_USER
    # si la contraseña no coincide devolver WRONG_PASSWD
    # cualquier otro caso devolver ERROR


if __name__ == '__main__':
    with open("db.json", mode='r') as file_handle:
        connection_data = JsonConnectionData(file_handle)
        connection = MongoConnectionHandle(data=connection_data)
        controller = LoginController(connection.connection().get_database("dbtest").get_collection("users"),
                                     hash_password)
        print(controller.user_exists("8113470034"))
        print(controller.login("8113470034", "20514920"))
