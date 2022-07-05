import json
from bson.json_util import dumps, loads

from dao import DAO
from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_visualization(DAO):

    def __init__(self, route="mongodb://localhost:27017"):
        """
        :Parameters:
            route: mongodb address, Default value: mongodb://localhost:27017
        """
        super().__init__(route)
        self.mongo = MongoClient(self.route)
        self.db_visualization = self.mongo.local.visualization_json

    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def deleteJSON(self, jsonId):
        """
        :Parameters:
            communityId: jsonId, Type: <class 'str'>
        """
        response = self.db_visualization.delete_one({'id': jsonId})

    def insertJSON(self, json):
        """
        :Parameters:
            communityJSON: json, Type: <class 'dict'>
        """
        temp = copy(json)
        response = self.db_visualization.insert_one(temp)

    def getJSONs(self):
        """
        :Return:
            Communities, Type: List[<class 'dict'>]
        """
        data = self.db_visualization.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getJSON(self, jsonId):
        """
        :Parameters:
            communityId: jsonId, Type: <class 'str'>
        :Return:
            Community, Type: <class 'dict'>
        """
        # data = self.db_visualization.find({"id": jsonId}, {"_id": 0})
        # data = loads(dumps(list(data)))
        # if len(data) == 0:
        #     return {}
        # return data[0]
        pass

    def replaceJSON(self, jsonId, newJSON):
        """
        :Parameters:
            communityId: jsonId, Type: <class 'str'>
            newJSON: JSON value, Type: <class 'dict'>
        """
        # temp = copy(newJSON)
        # response = self.db_visualization.replace_one({"id": jsonId}, temp)
        # return response
        pass


    def drop(self):
        """
            Mongo DB Drop Collection
        """
        self.db_visualization.drop()
