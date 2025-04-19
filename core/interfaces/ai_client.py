from abc import ABC, abstractmethod
from typing import Generator, Optional

class AIClient(ABC):
    """Interface for AI model clients"""
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generate text from prompt"""
        pass
                
    @abstractmethod
    def analyze_image(self, prompt: str, image_bytes: bytes) -> str:
        """Analyze image with prompt"""
        pass
    
    @abstractmethod
    def generate_image(self, prompt: str, negative_prompt: Optional[str] = None, 
                      style_preset: Optional[str] = None, seed: Optional[int] = None):
        pass