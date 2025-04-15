from models.image_processor import ImageProcessor
from services import ai_service
from ui.base_page import BasePage
import streamlit as st 

class ImageAnalysisPage(BasePage):
    """Image analysis page"""
    
    def render(self):
        """Render image analysis page"""
  
        image_bytes = ""
        st.subheader("Select an Image") 
        uploaded_file = st.file_uploader("Select an image", type=['png', 'jpeg'], label_visibility="collapsed")
        input_text = st.text_area("Input your question") 

        if uploaded_file:
            uploaded_image_preview = ImageProcessor.get_bytesio_from_bytes(uploaded_file.getvalue())
            image_bytes = uploaded_file.getvalue()

            st.image(uploaded_image_preview)

            go_button = st.button("Go", type="primary")

        if input_text and go_button: 
            response = self.ai_service.call_stream(input_text, image_bytes)
            st.write_stream(response)