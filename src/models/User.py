class User:
    def __init__(self, mobile_number):
        self.__mobile_number = mobile_number
        self.credit = None
        self.passwd_hash = None
