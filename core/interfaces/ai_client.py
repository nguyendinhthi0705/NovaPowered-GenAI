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
        