from typing import Generator
from core.interfaces.ai_client import AIClient

class ImageAnalysisService:
    """Service for image analysis operations"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    def analyze_image(self, prompt: str, image_bytes: bytes) -> Generator[str, None, None]:
        """Analyze image with prompt"""
        return self.ai_client.analyze_image(prompt, image_bytes)