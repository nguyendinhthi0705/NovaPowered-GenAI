from abc import ABC, abstractmethod
from typing import List, Dict, Generator

class KnowledgeBase(ABC):
    """Interface for knowledge base operations"""
    
    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search knowledge base"""
        pass
        
    @abstractmethod
    def search_and_generate(self, query: str) -> Generator[str, None, None]:
        """Search knowledge base and generate response"""
        pass