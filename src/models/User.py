class User:
    def __init__(self, mobile_number):
        self.__mobile_number = mobile_number
        self.credit = None
        self.verified = False
        self.passwd_salt = None
        self.passwd_hash = None

    def forDb(self):
        return {"mobile_number": self.__mobile_number, "salt": self.passwd_salt, "passwd": self.passwd_hash,
                "verified": self.verified, "credit": self.credit}
