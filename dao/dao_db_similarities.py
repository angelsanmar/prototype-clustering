import json
from bson.json_util import dumps, loads

from dao import DAO
from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_similarity(DAO):

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
        self.db_similarities = self.mongo.spiceComMod.similarities


    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def deleteSimilarity(self, target_community_id="", other_community_id=""):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>
        """
        if target_community_id != "":
            self.db_similarities.delete_one({'target-community-id': target_community_id})
        if other_community_id != "":
            self.db_similarities.delete_one({'other-community-id': other_community_id})

    def insertSimilarity(self, similarityJSON):
        """
        :Parameters:
            similarityJSON: similarity, Type: <class 'dict'>
        """
        temp = copy(similarityJSON)
        self.db_similarities.insert_one(temp)

    def getSimilarities(self):
        """
        :Return:
            Similarities, Type: List[<class 'dict'>]
        """
        data = self.db_similarities.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getSimilarity(self, target_community_id="", other_community_id=""):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>
        :Return:
            Similarity, Type: <class 'dict'>
        """
        data = {}
        if target_community_id != "":
            data = self.db_similarities.find({"target-community-id": target_community_id}, {"_id": 0})
        if other_community_id != "":
            data = self.db_similarities.find({"other-community-id": other_community_id}, {"_id": 0})

        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def updateSimilarity(self, target_community_id="", other_community_id="", newJSON={}):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>

            newJSON: JSON value, Type: <class 'dict'>
        """
        response = ""
        temp = copy(newJSON)
        if target_community_id != "":
            response = self.db_similarities.replace_one({"target-community-id": target_community_id}, temp)
        if other_community_id != "":
            response = self.db_similarities.replace_one({"other-community-id": other_community_id}, temp)
        return response


    def drop(self):
        """
            MongoDB Delete Documents in this collection
        """
        self.db_similarities.delete_many({})
