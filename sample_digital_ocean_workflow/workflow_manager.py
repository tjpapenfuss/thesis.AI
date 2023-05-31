# External packages
import json
from datetime import date
import os
import openai
import traceback
import time

#Internal packages
from config import OBJECT_STORAGE_KEY, OBJECT_STORAGE_SECRET, OBJECT_STORAGE_REGION, OBJECT_STORAGE_BUCKET
import spaces_upload
import database
import formata
import web_scrape 
import mongo_db_connector as mongo
import key_word_matcher
import doc_summarization

def error_logger(e, url):
    with open("error_log_summarization.txt", "a") as file:
        file.write(f"Invalid request error retrieving: {url}")
        file.write("Here is the error:\n")
        file.write(traceback.format_exc())
        file.write("\n")

def write_json_to_file(json_data, filename, directory):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the full file path
    filepath = os.path.join(directory, filename)

    # Write the JSON data to a .json file
    with open(filepath, 'w') as file:
        json.dump(json_data, file, indent=4)

s3config = {
    "region_name": OBJECT_STORAGE_REGION,
    "endpoint_url": "https://{}.digitaloceanspaces.com".format(OBJECT_STORAGE_REGION),
    "aws_access_key_id": OBJECT_STORAGE_KEY,
    "aws_secret_access_key": OBJECT_STORAGE_SECRET }

bucket_name = OBJECT_STORAGE_BUCKET

with open ('websites.txt', 'rt') as myfile:  # Open websites.txt for reading
    for myline in myfile:              # For each line, read to a string,
        url = myline.strip()        # Each line is a new URL to open and scrape
        start_time = time.time() # Start the timer to capture how long entire process takes. 
        
        # Step 1: Webpage Scraping
        page_text = web_scrape.extract_text_from_url(url)      
        url_cleaned = formata.clean_page(url)
        page_data = database.getpagedetails(url_cleaned)
        keywords = database.getkeywords()

        if page_data:
            page_data = page_data
        else:
            page_data = {'pid':'NOT FOUND/'+url_cleaned.replace("/","_"),'did':'domainid not found','orgid':'orgid not found'}

        if page_text:
            
            # Step 2: Data Transformation
            transformed_data = spaces_upload.transform_data(page_text)

            # Step 3: Storing Data in DigitalOcean Spaces
            object_name = str(page_data['pid'])
            orgid = str(page_data['orgid'])
            domainid = str(page_data['did'])
            today = str(date.today())
            # Set up the metadata to attach to the spaces storage
            metadata = {'URL': url, 'Ingestion_Date': today,'URL_cleaned':url_cleaned,'orgid':orgid,'domainid':domainid}
            spaces_upload.upload_to_spaces(bucket_name, object_name, transformed_data, 
                s3config["endpoint_url"], s3config["aws_access_key_id"], 
                s3config["aws_secret_access_key"], metadata = metadata)

            # Step 4: Get the keywords in the Website. Add in pid, orgid, and did. 
            keyword_JSON = key_word_matcher.count_keywords(page_text, keywords)
            keyword_JSON['URL']=url #Adding the URL to the JSON output
            keyword_JSON['PID']=object_name #Adding the PID to the output
            keyword_JSON['orgid']=orgid #Adding the Organization ID to the output
            keyword_JSON['did']=domainid #Adding the Domain ID to the output
            
            # Try to create the summary for a given document. If this fails, document it
            try:
                keyword_JSON["Summary"] = doc_summarization.summarize_doc(document=page_text)
            except openai.error.InvalidRequestError as e:
                keyword_JSON["Summary"] = "Failed to create the summary file for this website."
                error_logger(e, url=url)
            except Exception as e:
                keyword_JSON["Summary"] = "Failed to create the summary file for this website."
                error_logger(e, url=url)

            #print(today)
            json_output = json.dumps(keyword_JSON, indent=4)
            mongo.send_json_to_mongodb(json_data=json_output,orgid=orgid)

            # Create a summary for each webpage and write to JSON

            
            end_time = time.time()

            execution_time = end_time - start_time
            print(f"The website {url} took {execution_time} seconds to create.")

            # # Step 4: Storing Transformed Data in DigitalOcean Spaces
            # transformed_object_name = 'transformed_' + out_file_name
            # metadata = {'Author': 'John Doe', 'Timestamp': '2023-05-24'}
            # spaces_upload.upload_to_spaces(bucket_name, transformed_object_name, transformed_data, 
            #     s3config["endpoint_url"], s3config["aws_access_key_id"], 
            #     s3config["aws_secret_access_key"], Metadata = metadata)
