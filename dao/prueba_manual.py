import re
from dao import DAO
import os
from dao_db_users import DAO_db_users

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

    dao = DAO_db_users()
    dao.drop()
    user1 = {
        "id": "xxx",
        "userid": "001",
        "origin": "aaa",
        "source_id": "bbb",
        "age": "22",
        "gender": "F",
        "hobby": "bwm"
    }
    user2 = {
        "id": "xxx",
        "userid": "001",
        "origin": "aaa",
        "source_id": "bbb",
        "age": "19",
        "gender": "M",
        "religion": "AA"
    }
    correctResponse = {
        'userid': '001',
        'origin': 'aaa',
        'source_id': 'bbb',
        'hobby': 'bwm',
        'gender': 'M',
        'age': '19',
        'religion': 'AA'
    }
    dao.insertUser(user1)
    dao.updateUserPData(user2)
    # print(dao.getUser("001"))
    print(dao.getUsers())
    #dao.replaceUser(user1)




main()