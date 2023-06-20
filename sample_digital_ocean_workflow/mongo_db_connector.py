import pymongo
from pymongo import MongoClient
import json
import config
import re

def get_mongo_prod(name):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = config.mongo_string

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    #return document storage database
    return(client[name])

def get_collection(database,colname):
    # Connect to the MongoDB server
    client = pymongo.MongoClient(config.mongo_string)

    # Access the desired database
    db = client[config.MONGO_DATABASE]

    # Access the desired collection within the database
    collection = db[config.MONGO_COLLECTION]

    return(collection)

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

def get_pages_to_refine(database:'str',collection:'str'):
    collection = get_collection(database,collection)
    
    #identifies which key words to search for in pages to maximize high quality summaries
    keywords = ['/case/', '/study/', '/customer/', '/success/', '/partner/', '/solution/']
    pattern = '|'.join(map(re.escape, keywords))
    regex = re.compile(pattern, re.IGNORECASE)
    #runs search to find pages matching below logic: key words present in URL, page_text exists, page is in language, and page has not been refined.
    results = collection.find(
        {
        'page_url': {'$regex': regex},
        'page_text': {'$exists': True},
        'page_language': 'en',
        'refined': False
        },
        {
        'page_url': 1,
        'page_text': 1,
        '_id': 0
        }
    )
    #returns results
    if results:
        result_val = [item for item in results]
    else:
        result_val = None
    return(result_val)

def updateitem(database:'str',collection:'str',item_field:'str',item_value:'str',update_file:'dict'):
    collection = get_collection(database,collection)
    item_to_update = {item_field: item_value }
    updates = { "$set": update_file }
    collection.update_one(item_to_update, updates)

def get_refined(orgids:'list'):
    results = []
    for org in orgids:
        collection = get_collection(database=config.MONGO_DATABASE,colname=org)
        docs = collection.find({'refined':True},{'page_url':1,'summary':1,'keywords':1,'_id':0})
        for d in docs:
            results.append(d)
    return(results)

