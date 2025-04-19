from ui.base_page import BasePage
import streamlit as st
import io
from PIL import Image

class ImageGenerationPage(BasePage):
    """Image generation page using Amazon Nova Reel"""
    
    def __init__(self, title, image_generation_service):
        self.title = title
        super().__init__("Image Generation Page")
        self.image_generation_service = image_generation_service
    
    def render(self):
        """Render image generation page"""
        st.title("Image Generation with Amazon Nova Reel")
        st.write("Generate images using Amazon Nova Reel model")
        
        # Input for prompt
        prompt = st.text_area("Describe the image you want to generate", 
                             placeholder="A beautiful sunset over mountains with a lake in the foreground")
        
        # Advanced options in an expander
        with st.expander("Advanced Options"):
            negative_prompt = st.text_area("Negative Prompt (what to avoid in the image)", 
                                         placeholder="blurry, distorted, low quality", 
                                         help="Describe elements you don't want in the image")
            
            style_presets = ["None", "3d-model", "analog-film", "anime", "cinematic", "comic-book", 
                           "digital-art", "fantasy-art", "isometric", "line-art", "low-poly", 
                           "modeling-compound", "neon-punk", "origami", "photographic", "pixel-art", 
                           "tile-texture"]
            
            style_preset = st.selectbox("Style Preset", style_presets)
            if style_preset == "None":
                style_preset = None
                
            seed = st.number_input("Seed (for reproducibility)", 
                                 min_value=0, max_value=2147483647, 
                                 value=0, help="Set to 0 for random seed")
            if seed == 0:
                seed = None
        
        # Generate button
        if st.button("Generate Image", type="primary"):
            if not prompt:
                st.error("Please enter a prompt to generate an image")
            else:
                with st.spinner("Generating image..."):
                    try:
                        # Call the service to generate the image
                        image_bytes = self.image_generation_service.generate_image(
                            prompt=prompt,
                            negative_prompt=negative_prompt if negative_prompt else None,
                            style_preset=style_preset,
                            seed=seed
                        )
                        
                        # Display the generated image
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption="Generated Image", use_column_width=True)
                        
                        # Add download button
                        st.download_button(
                            label="Download Image",
                            data=image_bytes,
                            file_name="nova_canvas_generated.png",
                            mime="image/png"
                        )
                        
                    except Exception as e:
                        st.error(f"Error generating image: {str(e)}")
