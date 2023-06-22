from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, Document
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os
import config
import spaces_connector as spaces

# -----------------------------------------------------------------------------------------------------------------------------
# Function to build the index for OpenAI ChatBot. 
# Prereqs: 
#       - config.py containts the correct OpenAI api key; config.api_key
#       - config.py is configured with the connection string to the mongo DB; variable name -> mongo_string
#       - config.py is has the correct database to search to the mongo DB; variable name -> MONGO_DATABASE
#       - config.py has spaces configurations OBJECT_STORAGE_KEY, OBJECT_STORAGE_SECRET, OBJECT_STORAGE_REGION, and OBJECT_STORAGE_BUCKET
#       - SPACES_JSON_FILE_NAME is correct and uploaded into spaces. build_index_and_store.py uploads this file into Spaces.
# -----------------------------------------------------------------------------------------------------------------------------


os.environ["OPENAI_API_KEY"] = config.api_key

SPACES_JSON_FILE_NAME = "initial_index1.json"

def pull_json(file_name):
    #Configure s3 connection
    s3config = {
        "region_name": config.OBJECT_STORAGE_REGION,
        "endpoint_url": "https://{}.digitaloceanspaces.com".format(config.OBJECT_STORAGE_REGION),
        "aws_access_key_id": config.OBJECT_STORAGE_KEY,
        "aws_secret_access_key": config.OBJECT_STORAGE_SECRET,
        "bucket_name": config.OBJECT_STORAGE_BUCKET}

    file_location = "./" + file_name

    spaces.download_file_spaces(s3config["bucket_name"], file_name, 
        file_location, s3config["endpoint_url"], s3config["aws_access_key_id"], 
        s3config["aws_secret_access_key"])

def chatbot(input_text):

    # load the index 
    index = GPTSimpleVectorIndex.load_from_disk(SPACES_JSON_FILE_NAME)
    response = index.query(input_text, response_mode="compact")
    return response.response

def main():
    pull_json(SPACES_JSON_FILE_NAME)
    iface = gr.Interface(fn=chatbot,
                         inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                         outputs="text",
                         title="Custom-trained AI Chatbot")

    iface.launch(share=True)

if __name__ == "__main__":
    main()
