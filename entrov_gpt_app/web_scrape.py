import requests
from bs4 import BeautifulSoup
import traceback


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
            my_string = ""
            for element in job_elements:
                my_string = my_string + (element.get_text(strip=True)) + "\n"

            return my_string

        else:
            with open("error_log.txt", "a") as file:
                file.write(f"An error occurred while fetching content from URL: {url}. Status code: {response.status_code}")
                file.write("\n")
                print(f"An error occurred while fetching content from URL: {url}. Status code: {response.status_code}")
    except Exception as e:
        with open("error_log.txt", "a") as file:
            file.write(f"There was an error retrieving: {url}")
            file.write("Here is the error:\n")
            file.write(traceback.format_exc())
            file.write("\n")

# Webpage Scraping - simple
def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant text from the webpage
    scraped_data = soup.get_text()
    return scraped_data

