import json
import boto3
import base64
from typing import Dict, Generator, Optional
from core.interfaces.ai_client import AIClient
from infrastructure.ai.image_processor import ImageProcessor

class BedrockClient(AIClient):
    """Implementation of AIClient using Amazon Bedrock"""
    
    def __init__(self, model_id: str = "amazon.nova-pro-v1:0", region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id
        self.image_processor = ImageProcessor()
    
    def _create_request_body(self, prompt: str, image_bytes: Optional[bytes] = None, 
                           inference_params: Optional[Dict] = None) -> str:
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
        
    def generate_text(self, prompt: str) -> str:
        """Generate text from prompt"""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=self._create_request_body(prompt)
        )
        return response       
     
    def generate_text_stream(self, prompt: str) -> Generator[str, None, None]:
        """Generate text from prompt with streaming response"""
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=self._create_request_body(prompt)
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

    def analyze_image(self, prompt: str, image_bytes: bytes) -> str:
        """Analyze image with prompt"""
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=self._create_request_body(prompt, image_bytes)
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
            
    def generate_image(self, prompt: str, negative_prompt: Optional[str] = None, 
                      style_preset: Optional[str] = None, seed: Optional[int] = None) -> bytes:
        """Generate image using Amazon Nova Reel"""
        # Using Amazon Nova Reel model for image generation
        model_id = "amazon.nova-canvas-v1:0"
        
        # Prepare request body for image generation
        request_body = {
            "textToImageParams": {
            "text": prompt
            },
            "taskType": "TEXT_IMAGE",
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "height": 1024,
                "width": 1024,
                "cfgScale": 8.0
            }
        }
        
        # Add optional parameters if provided
        if negative_prompt:
            request_body["negativePrompt"] = negative_prompt
        if style_preset:
            request_body["imageGenerationConfig"]["stylePreset"] = style_preset
        if seed is not None:
            request_body["imageGenerationConfig"]["seed"] = seed
            
        # Invoke the model
        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        # Process the response
        response_body = json.loads(response.get("body").read())
        image_base64 = response_body.get("images")[0]
        
        # Convert base64 to bytes
        image_bytes = base64.b64decode(image_base64)
        return image_bytes
        
