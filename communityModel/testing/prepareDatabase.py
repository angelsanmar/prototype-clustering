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

from dao.dao_db_flags import DAO_db_flags


import json

def clear():
    daoF = DAO_db_flags("localhost", 27018, "spice", "spicepassword")
    daoF.drop()
    #daoF.insertFlag(True)
    
    daoC = DAO_db_community("localhost", 27018, "spice", "spicepassword")
    daoC.drop()
    daoC.dropFullList()

def initialize():
    daoPerspectives = DAO_db_perspectives("localhost", 27018, "spice", "spicepassword")
    daoPerspectives.drop()
    
    file = open("../perspectives/all.json")
    perspectives = json.load(file)
    print(perspectives)
    file.close()
    
    daoPerspectives.insertPerspective(perspectives)
    

clear()
#initialize()

[{'_id': {'$oid': '6323135a0215baeff4a9220b'}, 'id': '1', 'name': 'HEHCT Perspective', 'algorithm': {'name': 'agglomerative', 'params': []}, 'similarity_functions': [{'sim_function': {'name': 'HechtBeliefRSimilarityDAO', 'params': [], 'on_attribute': {'att_name': 'beleifR', 'att_type': 'String'}, 'weight': 0.8}}, {'sim_function': {'name': 'HechtBeliefJSimilarityDAO', 'params': [], 'on_attribute': {'att_name': 'beliefJ', 'att_type': 'String'}, 'weight': 0.6}}, {'sim_function': {'name': 'HechtDemographicReligiousSimilarityDAO', 'params': [], 'on_attribute': {'att_name': 'DemographicReligous', 'att_type': 'String'}, 'weight': 0.2}}, {'sim_function': {'name': 'HechtDemographicPoliticsSimilarityDAO', 'params': [], 'on_attribute': {'att_name': 'DemographicPolitics', 'att_type': 'String'}, 'weight': 0.2}}]}]


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
    
    
    