

import spaces_upload
import web_scrape 
from config import OBJECT_STORAGE_KEY, OBJECT_STORAGE_SECRET, OBJECT_STORAGE_REGION, OBJECT_STORAGE_BUCKET


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
        
        if page_text:
            #print(page_text)
            # Remove all special characters to save a new txt file. page_text[:8] is
            # the first 8 chars from the extracted URL text. 
            out_file_name = ''.join(e for e in page_text[:8] if e.isalnum()) + ".txt"
            #with open(out_file_name, "w", encoding="utf-8") as output_file:
                #output_file.write(page_text)
            
            # Step 2: Storing Data in DigitalOcean Spaces
            object_name = out_file_name
            spaces_upload.upload_to_spaces(bucket_name, object_name, page_text)
            print("Webpage " + url + "\nhas been successfully writen to file: " + out_file_name)

            # Step 3: Data Transformation
            transformed_data = spaces_upload.transform_data(page_text)

            # Step 4: Storing Transformed Data in DigitalOcean Spaces
            transformed_object_name = 'transformed_' + out_file_name
            metadata = {'Author': 'John Doe', 'Timestamp': '2023-05-24'}
            spaces_upload.upload_to_spaces(bucket_name, transformed_object_name, transformed_data, 
                s3config["endpoint_url"], s3config["aws_access_key_id"], 
                s3config["aws_secret_access_key"], Metadata = metadata)