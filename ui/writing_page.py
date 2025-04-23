from ui.base_page import BasePage
import streamlit as st 

class WritingPage(BasePage):
    def __init__(self, title, ai_service):
        self.title = title
        super().__init__("Writing Assistant", ai_service)
        
    def render(self):
        """Render writing page with multiple options"""
        st.markdown("# Writing Assistant")
        
        # Create a dropdown for selecting the writing feature
        writing_feature = st.selectbox(
            "Select Writing Feature",
            ["Improve Writing", "STAR Report", "Rewrite Content"]
        )
        
        # Display appropriate instructions based on selected feature
        if writing_feature == "Improve Writing":
            st.markdown("Input your content for writing improvement suggestions")
        elif writing_feature == "STAR Report":
            st.markdown("Input your report highlight for STAR format conversion")
        elif writing_feature == "Rewrite Content":
            st.markdown("Input your content to rewrite with stronger words")
        
        # Common input area
        input_text = st.text_area("", height=250)
        go_button = st.button("Go", type="primary")
        
        if input_text and go_button:
            # Call the appropriate service based on the selected feature
            if writing_feature == "Improve Writing":
                st.write_stream(self.text_generation.suggest_writing_improvements(input_text))
            elif writing_feature == "STAR Report":
                st.write_stream(self.text_generation.create_star_report(input_text))
            elif writing_feature == "Rewrite Content":
                st.write_stream(self.text_generation.rewrite_document(input_text))
