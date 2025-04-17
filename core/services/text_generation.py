from typing import Generator, Dict
from core.interfaces.ai_client import AIClient
from core.prompt_templates.templates import PromptTemplates

class TextGenerationService:
    """Service for text generation operations"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.templates = PromptTemplates()
    
    def chat(self, input_text: str) -> Generator[str, None, None]:
        """Chat"""
       
        prompt = self.templates.get_template("chat").format(content=input_text)
        print(prompt)
        return self.ai_client.generate_text_stream(prompt)
    
    def rewrite_document(self, input_text: str) -> Generator[str, None, None]:
        """Rewrite document with stronger words"""
        prompt = self.templates.get_template("rewrite").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def summarize(self, input_text: str) -> Generator[str, None, None]:
        """Summarize text"""
        prompt = self.templates.get_template("summary").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def create_star_report(self, input_text: str) -> Generator[str, None, None]:
        """Create STAR format report"""
        prompt = self.templates.get_template("star_report").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def suggest_writing_improvements(self, input_text: str) -> Generator[str, None, None]:
        """Suggest improvements for writing"""
        prompt = self.templates.get_template("improve_writing").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)