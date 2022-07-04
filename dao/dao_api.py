import json
from dao import DAO

import requests
from requests.auth import HTTPBasicAuth



class DAO_api(DAO):
    """
    outdated !!
    """
    def __init__(self, route=""):
        super().__init__(route)
        # self.route = route

    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def responseProcessing(self, response):
        """Process response from API"""
        if response.status_code == 400:
            return
        self.data = response.json()
        # self.data = json.dumps(self.data, sort_keys=True, indent=4)

    """__API for users__"""

    def userCommunities(self, userId):
        response = requests.get("http://spice.fdi.ucm.es/v1.1/users/{}/communities".format(userId))
        self.responseProcessing(response)
        return self.data, response

        # "Update community model with new user generated content"
        # tambien se puede llamar como updateUGC

    def updateUser(self, userId, ugc):
        response = requests.post("http://localhost:8080/v1.1/users/{}/update-generated-content".format(userId),
                                 json=ugc)
        # self.responseProcessing(response)
        return self.data, response

    """__API for communities__"""

    def communityList(self):
        response = requests.get("http://spice.fdi.ucm.es/v1.1/communities")
        self.responseProcessing(response)
        return self.data, response

    def communityDescription(self, communityId):
        response = requests.get("http://spice.fdi.ucm.es/v1.1/communities/{}".format(communityId))
        self.responseProcessing(response)
        return self.data, response

    def communityUsers(self, communityId):
        response = requests.get("http://spice.fdi.ucm.es/v1.1/communities/{}/users".format(communityId))
        self.responseProcessing(response)
        return self.data, response
