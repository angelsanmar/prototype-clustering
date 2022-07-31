from context import dao
from dao.dao_class import DAO
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub

import json

import requests
from requests.auth import HTTPBasicAuth

from bson.json_util import dumps, loads

def main():
    deleteAndLoad()

def deleteAndLoad():
    perspectives = [{
        "id": "100",
        "name": "Perspective_100",
        "algorithm": {
            "name": "String",
            "params": [
                "param_a", "param_b"
            ]
        },
        "similarity_functions": [{
            "sim_function": {
                "name": "String",
                "params": [
                    "param_a", "param_b"
                ],
                "on_attribute": {
                    "att_name": "String",
                    "att_type": "String"
                },
                "weight": 100
            }
        }]
    }, {
        "id": "101",
        "name": "Perspective_101",
        "algorithm": {
            "name": "String",
            "params": [
                "param_a", "param_b"
            ]
        },
        "similarity_functions": [{
            "sim_function": {
                "name": "String",
                "params": [
                    "param_a", "param_b"
                ],
                "on_attribute": {
                    "att_name": "String",
                    "att_type": "String"
                },
                "weight": 101
            }
        }]
    }]

    communities = [{
        "community-type": "explicit",
        "name": "elderly",
        "perspective": "Perspective_101",
        "explanation": "People above 65",
        "users": [
            "23",
            "28"
        ],
    }, {
        "community-type": "implicit",
        "explanation": "lorem ipsum",
        "perspective": "Perspective_101",
        "name": "impl_1",
        "users": [
            "44",
            "23"
        ]
    }, {
        "community-type": "explicit",
        "name": "teenager",
        "perspective": "Perspective_100",
        "explanation": "People whose age is between 12 and 17",
        "users": [
            "44",
            "56"
        ],
    }]

    similarities = [{
        "target-community-id": "621e53cf0aa6aa7517c2afdd",
        "other-community-id": "721e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.893,
    }, {
        "target-community-id": "721e53cf0aa6aa7517c2afdd",
        "other-community-id": "821e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.563,
    }, {
        "target-community-id": "621e53cf0aa6aa7517c2afdd",
        "other-community-id": "821e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.915,
    }, {
        "target-community-id": "721e53cf0aa6aa7517c2afdd",
        "other-community-id": "621e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.893,
    }, {
        "target-community-id": "821e53cf0aa6aa7517c2afdd",
        "other-community-id": "621e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.915,
    }, {
        "target-community-id": "821e53cf0aa6aa7517c2afdd",
        "other-community-id": "721e53cf0aa6aa7517c2afdd",
        "similarity-function": "cosine",
        "value": 0.563,
    }]

    daoP = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
    daoP.drop()
    daoP.insertPerspective(perspectives)

    daoC = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    daoC.drop()
    daoC.insertCommunity(communities)

    daoS = DAO_db_similarity("localhost", 27018, "spice", "spicepassword")
    daoS.drop()
    daoS.insertSimilarity(similarities)


main()
