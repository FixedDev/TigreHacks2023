import logging
from enum import Enum

from src.models.Login import hash_password
from src.models.db.DatabaseAccessController import MongoConnectionHandle, JsonConnectionData
from src.models.db.UserAccessObject import UserAccessObject
from src.models.User import User


class RegisterResult(Enum):
    SUCCESS = 1,
    INVALID_PASSWORD = 2,
    INVALID_PHONE = 3,
    ALREADY_EXISTS = 4,
    ERROR = 5


def validatePassword(password: str) -> bool:
    return len(password) >= 8


def validateNumber(number: str) -> bool:
    return len(number) >= 10


class SignUpController:
    db_access_object: UserAccessObject

    def __init__(self, db_access_object: UserAccessObject, password_hash_algor):
        self.db_access_object = db_access_object
        self.password_hash_algor = password_hash_algor

    def registerUser(self, mobile_phone, password):
        try:
            document = self.db_access_object.searchByNumber(mobile_phone)

            if document is not None:
                return RegisterResult.ALREADY_EXISTS

            if not validateNumber(mobile_phone):
                return RegisterResult.INVALID_PHONE

            if not validatePassword(password):
                return RegisterResult.INVALID_PASSWORD

            user = User(mobile_number=mobile_phone)
            (user.passwd_salt, user.passwd_hash) = self.password_hash_algor(password.encode("UTF-8"))

            self.db_access_object.insert(user.forDb())

            return RegisterResult.SUCCESS
        except Exception as e:
            logging.exception(e)
            return RegisterResult.ERROR


if __name__ == '__main__':
    with open("db.json", mode='r') as file_handle:
        connection_data = JsonConnectionData(file_handle)
        connection = MongoConnectionHandle(data=connection_data)
        user_access = UserAccessObject(connection.connection().get_database("dbtest").get_collection("users"))
        controller = SignUpController(user_access, hash_password)

        print(controller.registerUser("8113470034", "20514920"))
