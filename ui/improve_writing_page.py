from ui.base_page import BasePage
import streamlit as st 

class ImproveWritingPage(BasePage):
    def __init__(self, title, ai_service):
        self.title = title
        super().__init__("Improving Writing", ai_service)
        
    def render(self):
        """Render home page"""
        st.markdown("Input your content") 
        input_text = st.text_area("Input your question") 
        go_button = st.button("Go", type="primary")
        if input_text and go_button: 
            st.write_stream(self.text_generation.suggest_writing_improvements(input_text))
