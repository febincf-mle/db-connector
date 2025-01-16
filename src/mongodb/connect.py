from typing import Dict, Any, List

import certifi
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient, errors


ca = certifi.where()


class ConnectMongoDB:
    """
    A class to manage MongoDB connections and perform CRUD operations.
    """

    def __init__(self, uri: str = "mongodb://localhost:27017"):
        """
        Initialize the MongoDB connector.

        :param uri: MongoDB connection string (default: "mongodb://localhost:27017").
        """
        self.uri = uri
        self.client = None
        self.database = None
        self.collection = None

    def connect(self) -> None:
        """
        Establish a connection to the MongoDB server.
        """
        try:
            # use certifi
            self.client = MongoClient(self.uri, tlsCAFile=ca)
            print("Connected to MongoDB server successfully.")
        except errors.ConnectionError as e:
            raise ConnectionError(f"Failed to connect to MongoDB server: {e}")

    def set_database(self, database_name: str) -> None:
        """
        Set the active database.

        :param database_name: Name of the database to use.
        """
        if not self.client:
            raise ConnectionError("Client is not connected. Call `connect()` first.")
        try:
            self.database = self.client[database_name]
            print(f"Database set to: {database_name}")
        except Exception as e:
            raise ValueError(f"Failed to set database: {e}")

    def set_collection(self, collection_name: str) -> None:
        """
        Set the active collection.

        :param collection_name: Name of the collection to use.
        """
        if not self.database:
            raise ConnectionError("Database is not set. Call `set_database()` first.")
        try:
            self.collection = self.database[collection_name]
            print(f"Collection set to: {collection_name}")
        except Exception as e:
            raise ValueError(f"Failed to set collection: {e}")

    def insert_one(self, document: Dict[str, Any]) -> str:
        """
        Insert a single document into the current collection.

        :param document: The document to insert (as a dictionary).
        :return: The inserted document's ID.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            result = self.collection.insert_one(document)
            print(f"Document inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            raise ValueError(f"Failed to insert document: {e}")

    def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents into the current collection.

        :param documents: A list of documents to insert.
        :return: A list of inserted document IDs.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            result = self.collection.insert_many(documents)
            print(f"Inserted {len(result.inserted_ids)} document(s).")
            return result.inserted_ids
        except Exception as e:
            raise ValueError(f"Failed to insert documents: {e}")

    def find(self, query: dict = None, limit: int = 0) -> List[dict]:
        """
        Fetch multiple documents with an optional limit.

        :param query: The query filter (default: None, fetches all documents).
        :param limit: Maximum number of documents to fetch (default: 0, no limit).
        :return: A list of matching documents.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            query = query or {}
            cursor = self.collection.find(query)

            if len(limit) > 0:
                cursor = cursor.limit(5)
            
            documents = cursor.to_list()
            print(f"Fetched {len(documents)} document(s).")
            return documents
        except Exception as e:
            raise ValueError(f"Failed to fetch documents: {e}")

    def update_one(self, query: dict, update_data: dict) -> int:
        """
        Update a single document in the current collection.

        :param query: The query filter to match the document.
        :param update_data: The data to update (e.g., {"$set": {"field": "value"}}).
        :return: The count of modified documents.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            result = self.collection.update_one(query, update_data)
            print(f"Modified {result.modified_count} document(s).")
            return result.modified_count
        except Exception as e:
            raise ValueError(f"Failed to update document: {e}")

    def update_many(self, query: dict, update_data: dict) -> int:
        """
        Update multiple documents in the current collection.

        :param query: The query filter to match the documents.
        :param update_data: The data to update (e.g., {"$set": {"field": "value"}}).
        :return: The count of modified documents.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            result = self.collection.update_many(query, update_data)
            print(f"Modified {result.modified_count} document(s).")
            return result.modified_count
        except Exception as e:
            raise ValueError(f"Failed to update documents: {e}")

    def delete_one(self, query: dict) -> int:
        """
        Delete a single document from the current collection.

        :param query: The query filter to match the document.
        :return: The count of deleted documents.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            result = self.collection.delete_one(query)
            print(f"Deleted {result.deleted_count} document(s).")
            return result.deleted_count
        except Exception as e:
            raise ValueError(f"Failed to delete document: {e}")

    def delete_many(self, query: dict = None) -> int:
        """
        Delete multiple documents from the current collection.

        :param query: The query filter to match the documents (default: None, deletes all).
        :return: The count of deleted documents.
        """
        if not self.collection:
            raise ConnectionError("Collection is not set. Call `set_collection()` first.")
        try:
            query = query or {}
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} document(s).")
            return result.deleted_count
        except Exception as e:
            raise ValueError(f"Failed to delete documents: {e}")

    def close(self) -> None:
        """
        Close the connection to the MongoDB server.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")