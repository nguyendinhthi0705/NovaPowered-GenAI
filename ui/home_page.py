from ui.base_page import BasePage
import streamlit as st 

class HomePage(BasePage):
    def __init__(self, title, text_generation):
        self.title = title
        super().__init__("Home page", text_generation)
        
    def render(self):
        """Render home page"""

        st.markdown("Ask me anything") 
        input_text = st.text_area("Input your question") 
        go_button = st.button("Go", type="primary")
        if input_text and go_button: 
            st.write_stream(self.text_generation.chat(input_text))
