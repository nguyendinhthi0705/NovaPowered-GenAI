from ui.base_page import BasePage
import streamlit as st
import time
import config
import boto3
from PIL import Image
import io

class VideoGenerationPage(BasePage):
    """Video generation page using Amazon Nova Reel"""
    
    def __init__(self, title, video_generation_service):
        self.title = title
        super().__init__("Video Generation Page")
        self.video_generation_service = video_generation_service
    
    def render(self):
        """Render video generation page"""
        st.title("Video Generation with Amazon Nova Reel")
        st.write("Generate short videos using Amazon Nova Reel model")
        
        # Input for prompt
        prompt = st.text_area("Describe the video you want to generate", 
                             placeholder="A drone shot flying over mountains with a sunset in the background")
        
        # Video duration
        duration = st.slider("Video Duration (seconds)", 
                           min_value=2, 
                           max_value=config.MAX_VIDEO_DURATION, 
                           value=config.DEFAULT_VIDEO_DURATION, 
                           help="Select the duration of the generated video")
        
        # Advanced options in an expander
        with st.expander("Advanced Options"):
            negative_prompt = st.text_area("Negative Prompt (what to avoid in the video)", 
                                         placeholder="blurry, distorted, low quality", 
                                         help="Describe elements you don't want in the video")
                
            seed = st.number_input("Seed (for reproducibility)", 
                                 min_value=0, max_value=2147483647, 
                                 value=0, help="Set to 0 for random seed")
            if seed == 0:
                seed = 1
        
        # Generate button
        if st.button("Generate Video", type="primary"):
            if not prompt:
                st.error("Please enter a prompt to generate a video")
            else:
                # Create a placeholder for the job status
                status_placeholder = st.empty()
                status_placeholder.info("Submitting video generation job...")
                
                try:
                    # Submit the video generation job
                    invocation_arn = self.video_generation_service.generate_video(
                        prompt=prompt,
                        duration=duration,
                        negative_prompt=negative_prompt if negative_prompt else None,
                        seed=seed
                    )
                    
                    # Store job details in session state for tracking
                    st.session_state.video_job = invocation_arn
                    
                    # Update status
                    status_placeholder.success(f"Video generation job submitted successfully!")
                    st.info("Video generation typically takes 1-3 minutes. You can check the status below.")
                    st.info(f"Job started. Invocation ARN: {invocation_arn}")
                except Exception as e:
                    st.error(f"Error submitting video generation job: {str(e)}")
        
        # Check for existing job in session state and add a check status button
        if "video_job" in st.session_state:
            job_details = st.session_state.video_job
            st.subheader("Video Generation Job")
            
            # Add a check status button for the job
            if st.button("Check Status"):
                status_placeholder = st.empty()
                status_placeholder.info("Checking job status...")
                
                try:
                    # Check job status
                    response = self.video_generation_service.wait_for_video_completion(st.session_state.video_job)
                    current_status = response.get("status")
                    print(response)
                    if current_status == "Completed":
                        # Video is ready
                        status_placeholder.success("Video generation completed!")
                        
                        try:
                            # Generate a presigned URL for the video
                            video_url = response.get("url")
                            
                            # Display the video
                            st.video(response.get("url"))
                            
                            # Add download link
                            st.markdown(f"[Download Video]({video_url})")
                        except Exception as e:
                            st.error(f"Error retrieving video: {str(e)}")
                            st.info(f"The video should be available in S3 bucket: {current_status.get("s3uri")}, key: {config.S3_BUCKET_NAME}")
                        
                    elif current_status == "FAILED":
                        # Video generation failed
                        error_message = response.get("details", {}).get("errorMessage", "Unknown error")
                        status_placeholder.error(f"Video generation failed: {error_message}")
                        
                    else:
                        # Still in progress
                        status_placeholder.info(f"Video generation is still in progress. Status: {current_status}")
                        st.info("Please check back in a minute or two.")
                        
                except Exception as e:
                    status_placeholder.error(f"Error checking video status: {str(e)}")
                
        # Add information about Amazon Nova Reel
        with st.expander("About Amazon Nova Reel"):
            st.write("""
            Amazon Nova Reel is a generative AI model designed for creating short videos from text prompts.
            It can generate high-quality, creative videos based on your descriptions.
            
            Tips for better results:
            - Be specific and detailed in your prompts
            - Use descriptive adjectives for visual elements
            - Specify camera movements if desired (e.g., "drone shot", "panning camera")
            - Use the negative prompt to avoid unwanted elements
            
            Note: Video generation is an asynchronous process. After submitting a job, you'll need to check
            its status to see when it's complete. The video will be stored in an S3 bucket and available
            for viewing and download once ready.
            """)
