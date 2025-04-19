from abc import ABC, abstractmethod
from typing import Generator, Optional, Dict

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
        """Generate image from prompt"""
        pass
        
    @abstractmethod
    def generate_video(self, prompt: str, duration: int = 5, negative_prompt: Optional[str] = None, 
                      style_preset: Optional[str] = None, seed: Optional[int] = None) -> Dict:
        """Generate video from prompt (asynchronous)"""
        pass
        
    @abstractmethod
    def check_video_job_status(self, job_id: str) -> Dict:
        """Check the status of a video generation job"""
        pass