import json
from time import sleep
import mongo_db_connector
# Opening JSON file
f = open('/Users/tannerpapenfuss/thesis.AI/entrov_gpt_app/files_to_index/0c522e25-30c0-39fd-9580-debf361b4203.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

print(data['URL'])
data2 = (mongo_db_connector.get_mongodb_contents()[0])
data2 = json.loads(data2)
#print(f)
#data2 = json.load()

print(data2["keyword_counts"])

print(mongo_db_connector.get_all_collections())
json_list = []
for item in mongo_db_connector.get_mongodb_contents():
    item = json.loads(item)
    print(item["keyword_counts"])
    new_dict = {"Summary": item["Summary"], "keyword_counts": item["keyword_counts"]}
    json_list.append(new_dict)