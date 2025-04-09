from models.bedrock_client import BedrockClient
from services.ai_service import AIService
from services.knowledge_base_service import KnowledgeBaseService
from ui.home_page import HomePage


class NovaPoweredApp:
    """Main application class"""
    
    def __init__(self):
        self.bedrock_client = BedrockClient()
        self.ai_service = AIService(self.bedrock_client)
        self.kb_service = KnowledgeBaseService()
        self.home_page = HomePage("Home Page", self.ai_service)
        
    def run(self):
        """Run the application"""
        self.home_page.render()