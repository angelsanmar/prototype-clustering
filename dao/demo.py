from context import dao
from dao_class import DAO
import os

from context import dao
from dao.dao_class import DAO
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub

import json

import requests
from requests.auth import HTTPBasicAuth

from bson.json_util import dumps, loads



def main():
    daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
    daoUsers.drop()

    dao = DAO_api()
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

    # Hacemos post a la API. La API lo guarda en la db
    response = dao.updateUser(1, data_set)
    print(response.status_code)

    # Pedimos los datos desde la DAO Users, la DAO lee de db
    daoUsers = DAO_db_users("localhost", 27018, "spice", "spicepassword")
    print(daoUsers.getUser("1"))


main()
