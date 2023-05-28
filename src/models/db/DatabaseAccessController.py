from typing import Generic, TypeVar

import pymongo
from pymongo import *
import json


class ConnectionData:
    def loadFromFile(self, file):
        pass

    def __set(self, key, value):
        pass

    def __len__(self):
        pass

    def __getitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __reversed__(self):
        pass


class JsonConnectionData(ConnectionData):
    def __init__(self, file: object) -> None:
        self.values = json.load(file)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return reversed(self.values)


class ConnectionHandle:
    def __init__(self, data):
        pass

    def connection(self):
        pass


class MongoConnectionHandle(ConnectionHandle):
    def __init__(self, data: JsonConnectionData):
        super().__init__(data)
        self.__connection = MongoClient(host=data['host'],
                                        port=data['port'],
                                        **dict(data['other']))

    def connection(self):
        return self.__connection

