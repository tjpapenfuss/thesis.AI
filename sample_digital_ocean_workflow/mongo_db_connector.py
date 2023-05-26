import pymongo
import json
import config

def send_json_to_mongodb(json_data):
    # Parse JSON string to Python dictionary
    data = json.loads(json_data)

    # Connect to the MongoDB server
    client = pymongo.MongoClient(config.MONGO_CONN)

    # Access the desired database
    db = client[config.MONGO_DATABASE]

    # Access the desired collection within the database
    collection = db[config.MONGO_COLLECTION]

    # Insert the JSON data into the collection
    result = collection.insert_one(data)

    # Print the inserted document's ID
    print("Inserted document ID:", result.inserted_id)

# Example usage
# json_data = '{"name": "John", "age": 30}'
# send_json_to_mongodb(json_data)


def get_mongodb_contents():
    # Connect to the MongoDB server
    client = pymongo.MongoClient(config.MONGO_CONN)

    # Access the desired database
    db = client[config.MONGO_DATABASE]

    # Access the desired collection within the database
    collection = db[config.MONGO_COLLECTION]

    # Retrieve all documents from the collection
    documents = collection.find()

    # Convert documents to a list of JSON strings
    json_data = [json.dumps(doc, default=str) for doc in documents]

    return json_data

# Example usage
data = get_mongodb_contents()
for doc in data:
    print(doc)