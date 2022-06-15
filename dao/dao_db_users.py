from bson.json_util import dumps, loads

from dao import DAO
from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_users(DAO):

    def __init__(self, route="mongodb://localhost:27017"):
        """
        :Parameters:
            route: mongodb address, Default value: mongodb://localhost:27017>
        """
        super().__init__(route)
        self.mongo = MongoClient(self.route)
        self.db_users = self.mongo.local.users
        self.template = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx"
        }
        self.templateFull = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx",
            "source": "xxx",  # Not required
            "pname": "xxx",
            "pvalue": "xxx",
            "context": "xxx",  # Not required
            "datapoints": "xxx"  # Not required
        }
        self.templateWithoutP = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx",
            "source": "xxx",  # Not required
            "context": "xxx",  # Not required
            "datapoints": "xxx"  # Not required
        }

    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def insertUser(self, userJSON):
        """
        :Parameters:
            userJSON: JSON value, Type: <class ‘dict’>
        """
        user = copy(userJSON)
        userTemplate = self.template.copy()
        # temp["id"] = userJSON["id"]
        # temp["userid"] = userJSON["userid"]
        # temp["origin"] = userJSON["origin"]
        # temp["source_id"] = userJSON["source_id"]
        for key in userJSON.keys():  # anadimos los campos necesarios
            if key in self.template.keys():
                userTemplate[key] = userJSON[key]

        items = (userJSON.keys() - self.template.keys())
        for item in items:
            userPname = userTemplate.copy()
            userPname["pname"] = item
            userPname["pvalue"] = userJSON[item]
            self.db_users.insert_one(userPname)

    def getUsers(self):
        """
        :Return:
            List with all users, Type: list(<class 'dict'>)
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_users.find({})
        dataList = loads(dumps(list(dataList)))
        listUsersId = []
        for i in dataList:
            if i["userid"] not in listUsersId:
                listUsersId.append(i["userid"])
        listUsers = []
        for i in listUsersId:
            listUsers.append(self.getUser(i))
        return listUsers

    def getUser(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        :Return:
            User, Type: <class 'dict'>
        """
        # data = self.db_users.find({"userid": userId}, {"_id": 0})
        data = self.db_users.find({"userid": userId})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        else:
            user = self.template.copy()
            user["id"] = data[0]["_id"]
            user["userid"] = data[0]["userid"]
            user["origin"] = data[0]["origin"]
            user["source_id"] = data[0]["source_id"]
            for item in data:
                user[item["pname"]] = item["pvalue"]

        return user

    def updateUserPData(self, newJSON):
        user = self.getUser(newJSON["userid"])
        for item in newJSON.keys():
            if item not in self.templateWithoutP.keys():
                user[item] = newJSON[item]
        self.deleteUser(newJSON["userid"])
        self.insertUser(user)
        print(user)

    def replaceUser(self, newJSON):
        """
        :Parameters:
            newJSON: JSON value, Type: <class 'dict'>
        """
        self.deleteUser(newJSON["userid"])
        self.insertUser(newJSON)

    def deleteUser(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        """
        response = self.db_users.delete_many({"userid": userId})

    def drop(self):
        self.db_users.drop()
