from ui.base_page import BasePage
import streamlit as st 

class STARReportPage(BasePage):
    def __init__(self, title, ai_service):
        self.title = title
        super().__init__("Home page", )
        self.ai_service = ai_service
        
    def render(self):
        """Render home page"""
       
        st.markdown("Input your report high light") 
        input_text = st.text_area("") 
        go_button = st.button("Go", type="primary")
        if input_text and go_button: 
            st.write_stream(self.ai_service.create_STAR_Report(input_text))
