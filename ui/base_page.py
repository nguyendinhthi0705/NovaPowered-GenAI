from core.services.text_generation import TextGenerationService
from core.interfaces.ai_client import AIClient

import streamlit as st 

class BasePage:
    """Base class for all pages"""
    
    def __init__(self, title, text_generation= None):
        self.title = title
        super().__init__()
        self.text_generation = text_generation
        
    def setup(self):
        """Setup page configuration"""
        st.set_page_config(page_title=self.title)
        
    def render(self):
        """Render page content"""
        raise NotImplementedError("Subclasses must implement render()")