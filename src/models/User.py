from bson import ObjectId


def fromDocument(document):
    user = User(document['mobile_number'], document['_id'])
    user.credit = document['credit']
    user.verified = document['verified']
    user.passwd_hash = document['salt']
    user.passwd_hash = document['passwd']

    return user

class User:
    def __init__(self, mobile_number, id=ObjectId()):
        self.__id = id
        self.__mobile_number = mobile_number
        self.credit = 0
        self.verified = False
        self.passwd_salt = None
        self.passwd_hash = None

    def forDb(self):
        return {"_id": self.__id, "mobile_number": self.__mobile_number, "salt": self.passwd_salt,
                "passwd": self.passwd_hash,
                "verified": self.verified, "credit": self.credit}

    def id(self):
        return self.__id

    def mobile_number(self):
        return self.__mobile_number
