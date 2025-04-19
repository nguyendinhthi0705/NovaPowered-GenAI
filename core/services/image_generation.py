from typing import Optional
from core.interfaces.ai_client import AIClient

class ImageGenerationService:
    """Service for generating images using Amazon Nova Reel"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    def generate_image(self, prompt: str, negative_prompt: Optional[str] = None, 
                      style_preset: Optional[str] = None, seed: Optional[int] = None):
        """Generate image from prompt using Amazon Nova Reel"""
        return self.ai_client.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            style_preset=style_preset,
            seed=seed
        )
