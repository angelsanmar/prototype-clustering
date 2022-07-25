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
    data_set = [
        {
            "id": "11541",
            "userid": "1",
            "origin": "90e6d701748f08514b01",
            "source_id": "90e6d701748f08514b01",
            "source": "Content description",
            "pname": "DemographicGender",
            "pvalue": "F (for Female value)",
            "context": "application P:DemographicsPrep",
            "datapoints": 0
        },
        {
            "id": "11541",
            "userid": "1",
            "origin": "90e6d701748f08514b01",
            "source_id": "90e6d701748f08514b01",
            "source": "Content description",
            "pname": "Age",
            "pvalue": "22",
            "context": "application P:DemographicsPrep",
            "datapoints": 0
        }
    ]
    data_set2 = {
        "id": "11541",
        "userid": "1",
        "origin": "90e6d701748f08514b01",
        "source_id": "90e6d701748f08514b01",
        "source": "Content description",
        "pname": "DemographicGender",
        "pvalue": "F (for Female value)",
        "context": "application P:DemographicsPrep",
        "datapoints": 0,
        "communities": {1, 2, 3}
    }

    # daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
    # daoUsers.insertUser_API(data_set)
    #
    # daoCom = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    # dao = DAO_json('test/data/agglomerativeClusteringGAM.json')
    # daoCom.insertFileList("file0", dao.getData())

    data = {
        "id": "100",
        "name": "String",
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
    }

    dataShort1 = {
        "id": "100",
        "name": "String",
        "algorithm": "algorithm",
        "similarity_functions": "similarity_functions"
    }
    dataShort2 = {
        "id": "101",
        "name": "String",
        "algorithm": "algorithm",
        "similarity_functions": "similarity_functions"
    }

    daoP = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
    daoP.drop()
    daoP.insertPerspective(data)
    # daoP.insertPerspective(dataShort2)

    ## Prueba para el POST y el GET
    ## 8090 => local api server
    ## 8080 => spice api
    # response = requests.post("http://localhost:8090/", json=data_set)
    # response = requests.get("http://localhost:8090/json/file0")
    # response = requests.get("http://localhost:8090/json/all")
    # response = requests.get("http://localhost:8090/perspective/100")
    # response = requests.get("http://localhost:8090/thisRequestShouldReturn404Error")
    # response = requests.get("http://localhost:8090/index")
    response = requests.get("http://localhost:8080/v1.1/perspectives/100")
    print(response)
    print(response.text)
    print(response.status_code)
    print(response.headers)

    # # Prueba para insertar ficheros para la api y para db_community
    # daoCom = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    # dao = DAO_json('test/data/agglomerativeClusteringGAM.json')
    # daoCom.insertFileList("perspective0", dao.getData())

    ## Prueba para el POST y el GET
    # daoSim = DAO_db_similarity("localhost", 27018, "spice", "spicepassword")
    # daoSim.insertSimilarity(data_set2)
    # print(daoSim.getSimilarities())


main()
