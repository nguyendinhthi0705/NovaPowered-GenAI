from models.bedrock_client import BedrockClient
from services.ai_service import AIService
from services.knowledge_base_service import KnowledgeBaseService
from ui.home_page import HomePage
from ui.image_analysis_page import ImageAnalysisPage
from ui.star_report_page  import STARReportPage
from ui.improve_writing_page  import ImproveWritingPage
from ui.rewrite_page  import RewritePage

import streamlit as st 


class NovaPoweredApp:
    """Main application class"""
    
    def __init__(self):
        self.bedrock_client = BedrockClient()
        self.ai_service = AIService(self.bedrock_client)
        self.kb_service = KnowledgeBaseService()
        self.home_page = HomePage("Home Page", self.ai_service)
        self.image_analysis_page = ImageAnalysisPage("Image Analysis", self.ai_service)
        self.star_report_page = STARReportPage("STAR Report Page", self.ai_service)
        self.improve_writing = ImproveWritingPage("Improve Writing Page", self.ai_service)
        self.rewrite_page = RewritePage("Rewrite Page", self.ai_service)


    def run(self):
        """Run the application"""
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Select Page", ["Home", "Image Analysis", "STAR Report", "Improve Writing", "Rewrite"])
        if page == "Home":
            self.home_page.render()
        elif page == "Image Analysis":
            self.image_analysis_page.render()
        elif page == "STAR Report":
            self.star_report_page.render()
        elif page == "Improve Writing":
            self.improve_writing.render()
        elif page == "Rewrite":
            self.rewrite_page.render()