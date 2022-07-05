import re
from dao import DAO
import os

from dao_visualization import DAO_visualization
from api_visualization import API_visualization


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

    path1 = r"test/data/agglomerativeClusteringGAM.json"
    jsonFile = DAO_json(path1).getData()

    dao = DAO_visualization()
    dao.insertJSON(jsonFile)

    api = API_visualization()
    print(api.getData())


main()
