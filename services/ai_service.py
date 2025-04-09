import json
from models.bedrock_client import BedrockClient
from models.image_processor import ImageProcessor

class AIService:
    """Service for AI-related operations"""
    
    def __init__(self, bedrock_client=None):
        self.bedrock_client = bedrock_client or BedrockClient()
        self.image_processor = ImageProcessor()

    def call_stream(self, prompt, image=None):
        return self.bedrock_client.call_stream(prompt, image)
        
    def rewrite_document(self, input_text):
        """Rewrite document with stronger words"""
        prompt = """Your name is good writer. You need to rewrite content use stronger words to hight: 
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
        return self.call_stream(prompt)
        
    def summary_stream(self, input_text):
        prompt = f"""Based on the provided context, create summary the lecture
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
        return self.bedrock_client.call_stream(prompt)
        
    def query_document(self, question, docs):
        prompt = """Human: here is the content:
        <text>""" + str(docs) + """</text>
        Question: """ + question + """ 
    \n\nAssistant: """
        return self.bedrock_client.call_stream(prompt)
        
    def create_STAR_Report(self, input_text):
        prompt = """Your name is good writer. You need to rewrite content use stronger words to and format in STAR format: 
        \n\Content:
        <text>""" + str(input_text) + """</text>"""
        return self.bedrock_client.call_stream(prompt)
        
    def suggest_writing_document(self, input_text):
        prompt = """Your name is good writer. You need to suggest and correct mistake in the essay: 
        \n\nHuman: here is the content
        <text>""" + str(input_text) + """</text>
    \n\nAssistant: """
        return self.bedrock_client.call_stream(prompt)