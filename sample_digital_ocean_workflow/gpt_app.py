from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, Document
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
import time
import mongo_db_connector
import json
import config

os.environ["OPENAI_API_KEY"] = config.api_key

def construct_index(documents):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="compact")
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

json_list = []
for item in mongo_db_connector.get_mongodb_contents(collection = "orgid not found"):
    item = json.loads(item)
    new_string = str(item["URL"]) + str(item["Summary"]) + str(item["keyword_counts"])
    json_list.append(new_string)

documents = [Document(t) for t in json_list]

start_time = time.time()
index = construct_index(documents=documents)
end_time = time.time()

execution_time = end_time - start_time
print("The index took {} seconds to create.".format(execution_time))

iface.launch(share=True)