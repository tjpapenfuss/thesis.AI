
import web_scrape  
import os.path

import config
from datetime import date


with open ('websites.txt', 'rt') as myfile:  # Open websites.txt for reading
    for myline in myfile:              # For each line, read to a string,
        url = myline.strip()        # Each line is a new URL to open and scrape

        # Step 1: Webpage Scraping
        page_text = web_scrape.extract_text_from_url(url)
        
        if page_text:
            #print(page_text)
            # Remove all special characters to save a new txt file. page_text[:8] is
            # the first 8 chars from the extracted URL text. 
            out_file_name = ''.join(e for e in page_text[:20] if e.isalnum()) + ".txt"
            save_path = 'files_to_index/'
            completeName = os.path.join(save_path, out_file_name)         
            file1 = open(completeName, "w")
            file1.write(page_text)
            file1.close()