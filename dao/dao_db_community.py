import json
from bson.json_util import dumps, loads

from dao import DAO
from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_community(DAO):

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

        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS,
                                                                                           MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri)
        self.db_communities = self.mongo.spiceComMod.communities

    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def deleteCommunity(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        """
        response = self.db_communities.delete_one({'id': communityId})

    def insertCommunity(self, communityJSON):
        """
        :Parameters:
            communityJSON: Community, Type: <class 'dict'>
        """
        temp = copy(communityJSON)
        response = self.db_communities.insert_one(temp)

    def getCommunities(self):
        """
        :Return:
            Communities, Type: List[<class 'dict'>]
        """
        data = self.db_communities.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getCommunity(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        :Return:
            Community, Type: <class 'dict'>
        """
        data = self.db_communities.find({"id": communityId}, {"_id": 0})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def getCommunityUsers(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        :Return:
            Community users, Type: list[<class 'dict'>]
        """
        data = self.db_communities.find({"id": communityId}, {"users": 1, "_id": 0})
        return loads(dumps(list(data)))[0]

    def addUserToCommunity(self, communityId, newUser):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newUser: user, Type: <class 'dict'>
        """
        user = copy(newUser)
        response = self.db_communities.update_one(
            {"id": communityId},
            {
                "$push": {
                    "users": user
                }
            }
        )
        return response

    def replaceCommunity(self, communityId, newJSON):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newJSON: JSON value, Type: <class 'dict'>
        """
        temp = copy(newJSON)
        response = self.db_communities.replace_one({"id": communityId}, temp)
        return response

    def updateExplanation(self, communityId, newValue):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newValue: explanation, Type: <class 'str'>
        """
        value = copy(newValue)
        response = self.db_communities.update_one(
            {"id": communityId},
            {
                "$set": {
                    "explanation": value
                }
            },
            upsert = True
        )
        return response

    def drop(self):
        """
            Mongo DB Drop Collection
        """
        self.db_communities.drop()
