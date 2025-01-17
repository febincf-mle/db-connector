import os
import pytest
from bson import ObjectId

from connect_db.mongodb.connect import ConnectMongoDB


class TestConnectMongoDB:

    @pytest.fixture(scope="class")
    def mongo_connection(self):  

        connection_uri = os.getenv("MONGO_CONNECTION_URI")
        connector = ConnectMongoDB(connection_uri)
        connector.connect()

        yield connector

        connector.close()

    def test_set_database(self, mongo_connection):  
        mongo_connection.set_database("test_database")
        assert mongo_connection.database is not None
    
    def test_set_collection(self, mongo_connection):  
        mongo_connection.set_collection("test_collection")
        assert mongo_connection.collection is not None

    def test_insert_one(self, mongo_connection):  
        result = mongo_connection.insert_one({
            "name": "febin",
            "age": 20,
            "crush": "sandra"
        })

        assert isinstance(result, ObjectId)

    def test_insert_many(self, mongo_connection):  
        result = mongo_connection.insert_many([
            {
                "name": "ashwin",
                "age": 24,
                "crush": "shifana"
            },
            {
                "name": "ajith",
                "age": 23,
                "crush": "shahina"
            }
        ])

        assert type(result) == list
