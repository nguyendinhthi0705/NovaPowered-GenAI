import json
import boto3
from models.image_processor import ImageProcessor


class BedrockClient:
    """Handles communication with Amazon Bedrock"""
    
    def __init__(self, region="us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = "amazon.nova-pro-v1:0"
    
    def create_request_body(self, prompt, image_bytes=None, inference_params=None):
        """Create request body for Bedrock API"""
        if image_bytes:
            input_image_base64 = ImageProcessor.get_base64_from_bytes(image_bytes)
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
                "text": "Act as a chatbot assistant. You anwser the question they input in the same inout languages"
            }
        ]
        request_body = {
            "schemaVersion": "messages-v1",
            "messages": message_list,
            "system": system_list,
            "inferenceConfig": inf_params,
        }
        return json.dumps(request_body)
        
    def call_stream(self, prompt, image_bytes=None, inference_params=None):
        """Call Bedrock API with streaming response"""
        MODEL_ID = "amazon.nova-pro-v1:0"

        response = self.client.invoke_model_with_response_stream(
        modelId=MODEL_ID, body= self.create_request_body(prompt, image_bytes)
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