from bson.json_util import dumps, loads
from dao import DAO
from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_users(DAO):

    def __init__(self, MONGO_HOST="localhost", MONGO_PORT=27018, MONGO_USER="", MONGO_PASS="", MONGO_DB="spiceComMod"):
        """
        :Parameters:
            route: mongodb address, Default value: mongodb://localhost:27017
        """
        super().__init__(MONGO_HOST)
        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        self.db_users = self.mongo.spiceComMod.users
        self.template = {
            # "_id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx"
        }
        self.templateFull = {
            # "_id": "xxx",
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
            "_id": "xxx",
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
            userJSON: JSON value, Type: json <class 'dict'>
        """
        user = copy(userJSON)
        userTemplate = self.template.copy()
        for key in user.keys():  # anadimos los campos necesarios
            if key in self.template.keys():
                userTemplate[key] = user[key]

        items = (user.keys() - self.template.keys())
        for item in items:
            userPname = userTemplate.copy()
            userPname["pname"] = item
            userPname["pvalue"] = user[item]
            self.db_users.insert_one(userPname)

    def getUsers(self):
        """
        :Return:
            List with all users, Type: json List[<class 'dict'>]
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
            User, Type: json <class 'dict'>
        """
        # data = self.db_users.find({"userid": userId}, {"_id": 0})
        data = self.db_users.find({"userid": userId})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        else:
            user = self.template.copy()
            user["_id"] = data[0]["_id"]
            user["userid"] = data[0]["userid"]
            user["origin"] = data[0]["origin"]
            user["source_id"] = data[0]["source_id"]
            for item in data:
                user[item["pname"]] = item["pvalue"]

        return user

    def updateUser(self, newJSON):
        """
        :Parameters:
            newJSON: User/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        newData = copy(newJSON)
        if isinstance(newData, list):
            if len(newData) > 1:
                self.__updateMany(newData)
            else:
                self.__updateOne(newData[0])
        else:
            self.__updateOne(newData)

    def __updateOne(self, newData):
        # self.db_users.update_one({ "userid": newData["userid"], "pname": newData["pname"] }, newData, upsert = True)
        user = self.getUser(newData["userid"])
        del user["_id"]
        for item in newData.keys():
            if item not in self.templateWithoutP.keys():
                user[item] = newData[item]
        self.deleteUser(newData["userid"])
        self.insertUser(user)

    def __updateMany(self, newData):
        for user in newData:
            self.__updaneOne(user)

    def replaceUser(self, newJSON):
        """
        :Parameters:
            newJSON: User/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        newData = copy(newJSON)
        if isinstance(newData, list):
            if len(newData) > 1:
                self.__replaceUserMany(newData)
            else:
                self.__replaceUserOne(newData[0])
        else:
            self.__replaceUserOne(newData)

    def __replaceUserOne(self, newData):
        self.deleteUser(newData["userid"])
        self.insertUser(newData)

    def __replaceUserMany(self, newData):
        for user in newData:
            self.__replaceUserOne(user)

    def deleteUser(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        """
        response = self.db_users.delete_many({"userid": userId})

    def drop(self):
        """
            Mongo DB Drop Collection
        """
        self.db_users.drop()
