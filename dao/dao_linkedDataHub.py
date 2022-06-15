import json
from dao import DAO

import requests
from requests.auth import HTTPBasicAuth


class DAO_linkedDataHub(DAO):
    def __init__(self, route="https://api2.mksmart.org/object/89b71c31-4bd3-44ad-9573-420e6320e945"):
        super().__init__(route)
        self.response = None

    def getData(self):
        return self.data, self.response

    def extractData(self):
        uuid = "xxx"
        self.response = requests.get(self.route, auth=HTTPBasicAuth(uuid, uuid))
        if self.response.status_code == 200:
            self.data = self.response.json()
        else:
            self.data = ""
            raise Exception('LinkedDataHub response != "200"')

