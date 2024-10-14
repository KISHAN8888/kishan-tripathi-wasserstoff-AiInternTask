from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CollectionInvalid
import logging
import json
from bson.objectid import ObjectId
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, connection_string='mongodb://localhost:27017', db_name='pdf_summary_db'):
        self.client = None
        self.db = None
        self.connection_string = connection_string
        self.db_name = db_name

    def connect(self):
        """Establish a connection to MongoDB."""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # the ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.db = self.client[self.db_name]
            logging.info("Successfully connected to MongoDB.")
        except ConnectionFailure as e:
            logging.error(f"Server not available. Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while connecting to MongoDB: {e}")
            raise

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logging.info("Closed connection to MongoDB.")

    def insert_document(self, collection_name, document):
        """
        Insert a document into the specified collection.
        
        :param collection_name: Name of the collection
        :param document: Document to insert
        :return: Inserted document ID
        """
        if self.db is None:
            raise ConnectionError("Database connection not established. Call connect() first.")
        
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        logging.info(f"Inserted document with ID: {result.inserted_id}")
        return result.inserted_id

    def update_document(self, collection_name, query, update):
        """
        Update a document in the specified collection.
        
        :param collection_name: Name of the collection
        :param query: Query to find the document to update
        :param update: Update operations to apply
        :return: UpdateResult object
        """
        if self.db is None:
            raise ConnectionError("Database connection not established. Call connect() first.")
        
        collection = self.db[collection_name]
        result = collection.update_one(query, update)
        logging.info(f"Modified {result.modified_count} document(s)")
        return result

    def find_document(self, collection_name, query):
        """
        Find a document in the specified collection.
        
        :param collection_name: Name of the collection
        :param query: Query to find the document
        :return: Found document or None
        """
        if self.db is None:
            raise ConnectionError("Database connection not established. Call connect() first.")
        
        collection = self.db[collection_name]
        return collection.find_one(query)

document_schema = {
    "filename": str,
    "path": str,
    "num_pages": int,
    "author": str,
    "creation_date": str,
    "file_size": int,
    "summary": str,
    "keywords": str,
    "processing_status": str,
    "last_updated": str
}

def create_document_schema(db_manager):
    """Create a schema for the documents collection."""
    if db_manager.db is None:
        raise ConnectionError("Database connection not established. Call connect() first.")
    
    try:
        db_manager.db.create_collection("documents")
        logging.info("Created 'documents' collection.")
    except CollectionInvalid:
        logging.info("Collection 'documents' already exists. Updating schema.")

    db_manager.db.command("collMod", "documents", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["filename", "path", "num_pages", "processing_status", "last_updated"],
            "properties": {
                "filename": {"bsonType": "string"},
                "path": {"bsonType": "string"},
                "num_pages": {"bsonType": "int"},
                "author": {"bsonType": "string"},
                "creation_date": {"bsonType": "string"},
                "file_size": {"bsonType": "int"},
                "summary": {"bsonType": "string"},
                "keywords": {"bsonType": "string"},
                "processing_status": {"bsonType": "string"},
                "last_updated": {"bsonType": "string"}
            }
        }
    })
    logging.info("Updated 'documents' collection schema.")



if __name__ == "__main__":
    db_manager = DatabaseManager(connection_string='mongodb://localhost:27017')
    try:
        db_manager.connect()
        create_document_schema(db_manager)
        
        # Example of inserting a document
        doc = {
            "filename": "example.pdf",
            "path": "/path/to/example.pdf",
            "num_pages": 10,
            "author": "John Doe",
            "creation_date": "2023-01-01",
            "file_size": 1024000,
            "processing_status": "pending",
            "last_updated": "2023-10-09T12:00:00Z"
        }
        doc_id = db_manager.insert_document("documents", doc)
        print(f"Inserted document ID: {doc_id}")
        
        # Example of updating a document
        update_result = db_manager.update_document(
            "documents",
            {"filename": "example.pdf"},
            {"$set": {"processing_status": "completed"}}
        )
        print(f"Updated {update_result.modified_count} document(s)")
        
        # Example of finding a document
        found_doc = db_manager.find_document("documents", {"filename": "example.pdf"})
        print(f"Found document: {found_doc}")
        
    except ConnectionFailure:
        logging.error("Could not connect to MongoDB. Please check if the server is running.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if db_manager.client:
            db_manager.close()
