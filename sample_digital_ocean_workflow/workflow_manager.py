import spaces_upload
import web_scrape 
import mongo_db_connector
import json

from config import OBJECT_STORAGE_KEY, OBJECT_STORAGE_SECRET, OBJECT_STORAGE_REGION, OBJECT_STORAGE_BUCKET
from datetime import date
import database
import formata
import key_word_matcher


s3config = {
    "region_name": OBJECT_STORAGE_REGION,
    "endpoint_url": "https://{}.digitaloceanspaces.com".format(OBJECT_STORAGE_REGION),
    "aws_access_key_id": OBJECT_STORAGE_KEY,
    "aws_secret_access_key": OBJECT_STORAGE_SECRET }

bucket_name = OBJECT_STORAGE_BUCKET

with open ('websites.txt', 'rt') as myfile:  # Open websites.txt for reading
    for myline in myfile:              # For each line, read to a string,
        url = myline.strip()        # Each line is a new URL to open and scrape

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
            #print(page_text)
            # Remove all special characters to save a new txt file. page_text[:8] is
            # the first 8 chars from the extracted URL text. 
            keyword_JSON = key_word_matcher.count_keywords(page_text, keywords)
            json_output = json.dumps(keyword_JSON, indent=4)
            out_file_name = ''.join(e for e in page_text[:8] if e.isalnum()) + ".txt"
            #with open(out_file_name, "w", encoding="utf-8") as output_file:
                #output_file.write(page_text)
            
            # Step 2: Data Transformation
            transformed_data = spaces_upload.transform_data(page_text)

            # Step 3: Storing Data in DigitalOcean Spaces
            # object_name = out_file_name
            object_name = str(page_data['pid'])
            orgid = str(page_data['orgid'])
            domainid = str(page_data['did'])
            today = str(date.today())
            #print(today)
            metadata = {'URL': url, 'Ingestion_Date': today,'URL_cleaned':url_cleaned,'orgid':orgid,'domainid':domainid}
            spaces_upload.upload_to_spaces(bucket_name, object_name, transformed_data, 
                s3config["endpoint_url"], s3config["aws_access_key_id"], 
                s3config["aws_secret_access_key"], metadata = metadata)
            print("Webpage " + url + "\nhas been successfully writen to file: " + out_file_name)
            send_json_to_mongodb(json_data=keyword_json,orgid=orgid)
            print("mongo file upload done")


            # # Step 4: Storing Transformed Data in DigitalOcean Spaces
            # transformed_object_name = 'transformed_' + out_file_name
            # metadata = {'Author': 'John Doe', 'Timestamp': '2023-05-24'}
            # spaces_upload.upload_to_spaces(bucket_name, transformed_object_name, transformed_data, 
            #     s3config["endpoint_url"], s3config["aws_access_key_id"], 
            #     s3config["aws_secret_access_key"], Metadata = metadata)