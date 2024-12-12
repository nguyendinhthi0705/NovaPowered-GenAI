import os
import boto3, json
from dotenv import load_dotenv
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain_community.chat_models import BedrockChat
from datetime import datetime
import base64
from io import BytesIO

load_dotenv()

def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    return image_io


def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes

def init(prompt, image_bytes=None):  

    if image_bytes:
        input_image_base64 = get_base64_from_bytes(image_bytes)
        message_list = [
            {   
                "role": "user", 
                "content": [                
                    {
                        "image":{
                            "format" : "jpeg" ,
                            "source":{
                                "bytes": input_image_base64
                            }
                        }
                    },
                     {"text": prompt},
                    ]
            }]
    else:
        message_list = [{"role": "user", "content": [{"text": prompt}]}]
   
    inf_params = {"max_new_tokens": 5000, "top_p": 0.1, "top_k": 20, "temperature": 0.3}

    system_list = [
            {
                "text": "Act as a chatbot assistant. You anwser the question they input."
            }
    ]
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params,
    }
    return json.dumps(request_body)

def call_stream(prompt, image = None):

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    MODEL_ID = "amazon.nova-pro-v1:0"

    response = client.invoke_model_with_response_stream(
    modelId=MODEL_ID, body= init(prompt, image)
    )
    request_id = response.get("ResponseMetadata").get("RequestId")
    print(f"Request ID: {request_id}")
    print("Awaiting first token...")

    chunk_count = 0
    stream = response.get("body")


    if stream:
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                chunk_json = json.loads(chunk.get("bytes").decode())
                content_block_delta = chunk_json.get("contentBlockDelta")
                if content_block_delta:
                    chunk_count += 1
                    yield content_block_delta.get("delta").get("text")
        print(f"Total chunks: {chunk_count}")
    else:
        print("No response stream received.")
   
    
def rewrite_document(input_text): 
    prompt = """Your name is good writer. You need to rewrite content use stronger words to hight: 
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
    return call_stream(prompt)


def summary_stream(input_text):     
    prompt = f"""Based on the provided context, create summary the lecture
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
    return call_stream(prompt)

def query_document(question, docs): 
    prompt = """Human: here is the content:
        <text>""" + str(docs) + """</text>
        Question: """ + question + """ 
    \n\nAssistant: """

    return call_stream(prompt)

def create_STAR_Report(input_text): 
    prompt = """Your name is good writer. You need to rewrite content use stronger words to and format in STAR format: 
        \n\Content:
        <text>""" + str(input_text) + """</text>"""
    return call_stream(prompt)

def suggest_writing_document(input_text): 
    prompt = """Your name is good writer. You need to suggest and correct mistake in the essay: 
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
    return call_stream(prompt)

def search(prompt):    
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id = "ENJIY1A7GT", 
        top_k = 3,
        retrieval_config = {
            "vectorSearchConfiguration": {
                "numberOfResults": 5, 
                'overrideSearchType': "SEMANTIC"
            }
        }
    )
    
    retrieved_docs = retriever.get_relevant_documents(prompt + " 2024")
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    system_prompt = f"""
    Based on the provided context, provide the answer to the following question:
    <context>{context}</context>
    <question>{prompt} </question>
"""
    print (system_prompt)
    return call_stream(system_prompt)
