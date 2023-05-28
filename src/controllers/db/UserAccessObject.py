import logging

import pymongo

from src.models.User import User, fromDocument


class UserAccessObject:
    db_access_object: pymongo.collection

    def __init__(self, db_access_object: pymongo.collection):
        self.db_access_object = db_access_object

    def search(self, filter):
        document = self.db_access_object.find_one(filter)

        if document is None:
            return None

        user = fromDocument(document)
        return user

    def searchByNumber(self, number):
        return self.search({"mobile_number": number})

    def searchById(self, id):
        return self.search({"_id": id})

    def insert(self, user: User):
        self.db_access_object.insert_one(user.forDb())

    def update(self, user: User):
        self.db_access_object.update_one(filter={"_id": user.id()}, update=user.forDb())
