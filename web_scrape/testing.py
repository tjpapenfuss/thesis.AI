import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        # Send a request to the specified URL. 
        response = requests.get(url)

        # If the request succeeded, move further. If the request fails, print the error code. 
        if response.status_code == 200:
            # Parse the obtained HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            results = soup.find(id="ResultsContainer")
            job_elements = soup.find_all(['h1', 'h2', 'h3', 'p'])
            #print(job_elements)
            my_string = ""
            for element in job_elements:
                #my_string.join("-----------------------------------------\n" + element + 
                #"-----------------------------------------\n")
                my_string = my_string + (element.get_text(strip=True)) + "\n"

            # Not using any of the below, except return statment. 

            # Remove script and style elements (as they won't have any useful text)
            # for script_style_element in soup(['script', 'style']):
            #     script_style_element.extract()

            # raw_text = soup.get_text()

            # # Eliminate unwanted whitelines
            # lines = [x.strip() for x in raw_text.split("\n") if x.strip()]
            # final_text = "\n".join(lines)
            #print(my_string)
            #return final_text
            return my_string

        else:
            print(f"An error occurred while fetching content from URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    with open ('websites.txt', 'rt') as myfile:  # Open lorem.txt for reading
        for myline in myfile:              # For each line, read to a string,
            url = myline.strip()
            #print("Here is the website: " + myline + "END OF WEB")                  # and print the string.

            page_text = extract_text_from_url(url)
            
            if page_text:
                #print(page_text)
                # Remove all special characters to save a new txt file. page_text[:8] is
                # the first 8 chars from the extracted URL text. 
                out_file_name = ''.join(e for e in page_text[:8] if e.isalnum()) + ".txt"
                with open(out_file_name, "w", encoding="utf-8") as output_file:
                    output_file.write(page_text)
                print("Webpage " + url + "\nhas been successfully writen to file: " + out_file_name)