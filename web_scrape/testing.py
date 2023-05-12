import requests

# URL = "https://aws.amazon.com/solutions/case-studies/caremonitor/"
# page = requests.get(URL)

# print(page.text)

import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        # Send a request to the specified URL
        response = requests.get(url)

        # If the request succeeded, move further
        if response.status_code == 200:
            # Parse the obtained HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # results = soup.find(id="ResultsContainer")
            # job_elements = soup.find_all()
            # #print(job_elements)
            # for job_element in job_elements:
            #     title_element = job_element.find("h2")
            #     company_element = job_element.find("h3")
            #     location_element = job_element.find("p")
            #     print(title_element)
            #     print(company_element)
            #     print(location_element)

            # Remove script and style elements (as they won't have any useful text)
            for script_style_element in soup(['script', 'style']):
                script_style_element.extract()

            raw_text = soup.get_text()

            # Eliminate unwanted whitelines
            lines = [x.strip() for x in raw_text.split("\n") if x.strip()]
            final_text = "\n".join(lines)

            return final_text

        else:
            print(f"An error occurred while fetching content from URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    url = "https://aws.amazon.com/solutions/case-studies/caremonitor/" # Replace this with the desired url

    page_text = extract_text_from_url(url)
    
    if page_text:
        #print(page_text)
        with open("output.txt", "w", encoding="utf-8") as output_file:
            output_file.write(page_text)