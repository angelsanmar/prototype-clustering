import re
from dao import DAO
import os
from dao_db_users import DAO_db_users
from dao_db_community import DAO_db_community

from dao_csv import DAO_csv
from dao_json import DAO_json
from dao_api import DAO_api
from dao_linkedDataHub import DAO_linkedDataHub
import json

import requests
from requests.auth import HTTPBasicAuth

from bson.json_util import dumps, loads

from dao import DAO


def main():

    dao = DAO_api()
    data_set = [
                  {
                    "id": "23",
                    "userid": "23",
                    "origin": "90e6d701748f08514b01",
                    "source_id": "90e6d701748f08514b01",
                    "source": "Content description",
                    "pname": "DemographicGender",
                    "pvalue": "F (for Female value)",
                    "context": "application P:DemographicsPrep",
                    "datapoints": 0
                  }
                ]
    json_dump = json.dumps(data_set)

    data, response = DAO_api().updateUser(23, data_set)
    print(response.status_code)






main()