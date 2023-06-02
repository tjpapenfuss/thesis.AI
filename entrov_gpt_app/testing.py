import json
from time import sleep
import mongo_db_connector
# Opening JSON file
f = open('/Users/tannerpapenfuss/thesis.AI/entrov_gpt_app/files_to_index/6bc08c82-570b-39f3-980d-1f8b53c334ca.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

print(data['URL'])
data2 = (mongo_db_connector.get_mongodb_contents()[0])
data2 = json.loads(data2)
#print(f)
#data2 = json.load()

print(data2["keyword_counts"])
print("GETTING KEYS")
print(data2["keyword_counts"].keys())
key_word_string = "This document contains the following reference keys: "
for key in data2["keyword_counts"].keys():
    key_word_string = key_word_string + key + ", "

print(key_word_string)
# print(mongo_db_connector.get_all_collections())
# json_list = []
# for item in mongo_db_connector.get_mongodb_contents():
#     item = json.loads(item)
#     print(item["keyword_counts"])
#     new_dict = {"Summary": item["Summary"], "keyword_counts": item["keyword_counts"]}
#     json_list.append(new_dict)