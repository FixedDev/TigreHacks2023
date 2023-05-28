import logging
from enum import Enum

from bcrypt import *

from src.models.User import User
from src.models.db.UserAccessObject import UserAccessObject


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


class LoginManagement:
    def __init__(self, db_access_object: UserAccessObject, password_hash_algor):
        self.db_access_object = db_access_object
        self.password_hash_algor = password_hash_algor

    def user_exists(self, mobile_number):
        return self.db_access_object.searchByNumber(mobile_number) is not None

    def login(self, mobile_number, password) -> (LoginResult, User):
        try:
            user = self.db_access_object.searchByNumber(mobile_number)

            if user is None:
                return LoginResult.USER_NOT_EXISTS, None

            return (LoginResult.SUCCESS, user) if checkIfValid(password.encode("UTF-8"), user) else (LoginResult.WRONG_PASSWORD, None)
        except Exception as e:
            logging.exception(e)
            return LoginResult.ERROR, None

    # db_access_object.search({name: user_name}).then(__check_if_valid)
    # si es valido, devolver un SUCCESS, si el usuario no se encuentra, INVALID_USER
    # si la contraseña no coincide devolver WRONG_PASSWD
    # cualquier otro caso devolver ERROR


