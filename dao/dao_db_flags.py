from bson.json_util import dumps, loads


from context import dao
from dao.dao_class import DAO

from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_flags(DAO):

    def __init__(self, MONGO_HOST="localhost", MONGO_PORT=27018, MONGO_USER="", MONGO_PASS="", MONGO_DB="spiceComMod"):
        """
        :Parameters:
            MONGO_HOST: mongodb address, Default value: "localhost"
            MONGO_PORT: mongodb port, Default value: 27018
            MONGO_USER: mongodb user, Default value: ""
            MONGO_PASS: mongodb pass, Default value: ""
            MONGO_DB: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__(MONGO_HOST)
        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS,
                                                                                           MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        self.db_flags = self.mongo.spiceComMod.flags


    def getData(self):
        pass

    def insertFlag(self, value):
        data = {"flag": value}

        self.db_flags.insert_one(data)


    def getFlag(self):
        """
        :Return:
            List with all users, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_flags.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList[0]



    def invertFlag(self):
        """
        :Parameters:
            newJSON: User/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        data = self.getFlag()
        self.drop()
        if data["flag"] == True:
            self.insertFlag(False)
        else:
            self.insertFlag(True)




    def deleteFlag(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        """
        self.db_flags.delete_many({"userid": userId})

    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_flags.delete_many({})
