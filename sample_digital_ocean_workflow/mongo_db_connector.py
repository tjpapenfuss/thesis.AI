import pymongo
from pymongo import MongoClient
import json
import config

def get_mongo_prod(name):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config.mongo_string

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    #return document storage database
    return(client[name])

def get_collection(colname):
    #get database from document storage
    database = get_mongo_prod('Key_words')
    
    #return collection from identified database
    return(database[colname])

print(get_mongo_prod('Key_words'))

def send_json_to_mongodb(json_data,orgid):
    # Parse JSON string to Python dictionary
    data = json.loads(json_data)

    # Access the desired collection within the database
    collection = get_collection(orgid)


    # Check if the record exists in the collection
    existing_record = collection.find_one({"PID": data["PID"]})

    if existing_record:
        # Record already exists, perform update/overwrite
        result = collection.replace_one({"PID": data["PID"]}, data)
        print("Record updated:", existing_record["_id"])
    else:
        # Record doesn't exist, perform insert
        result = collection.insert_one(data)
        print("Record created:", result.inserted_id)

    # Insert the JSON data into the collection
    # result = collection.insert_one(data)

    # Print the inserted document's ID
    # print("Inserted document ID:", result.inserted_id)

# Example usage
#json_data = '{"name": "John", "age": 30,"orgid":"1234"}'
#send_json_to_mongodb(json_data,orgid)


def get_mongodb_contents(collection=config.MONGO_COLLECTION):
    # Connect to the MongoDB server
    client = pymongo.MongoClient(config.mongo_string)

    # Access the desired database
    db = client[config.MONGO_DATABASE]

    # Access the desired collection within the database
    collection = db[collection]

    # Retrieve all documents from the collection
    documents = collection.find()

    # Convert documents to a list of JSON strings
    json_data = [json.dumps(doc, default=str) for doc in documents]

    return json_data

# Example usage
#data = get_mongodb_contents()
#for doc in data:
#    print(doc)