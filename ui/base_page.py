from services.ai_service import AIService
import streamlit as st 

class BasePage:
    """Base class for all pages"""
    
    def __init__(self, title, ai_service=None):
        self.title = title
        super().__init__()
        self.ai_service = ai_service or AIService()
        
    def setup(self):
        """Setup page configuration"""
        st.set_page_config(page_title=self.title)
        
    def render(self):
        """Render page content"""
        raise NotImplementedError("Subclasses must implement render()")