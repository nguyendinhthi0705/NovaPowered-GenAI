from typing import Optional, Dict
import time
import boto3
from core.interfaces.ai_client import AIClient
import config

class VideoGenerationService:
    """Service for generating videos using Amazon Nova Reel"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.s3_client = boto3.client('s3', region_name=config.AWS_REGION)
    
    def generate_video(self, prompt: str, duration: int = 5, 
                      negative_prompt: Optional[str] = None, 
                      style_preset: Optional[str] = None, 
                      seed: Optional[int] = None) -> Dict:
        """
        Generate video from prompt using Amazon Nova Reel
        
        This is an asynchronous operation. It returns job details that can be used
        to check status and retrieve the video when ready.
        """
        return self.ai_client.generate_video(
            prompt=prompt,
            duration=duration,
            negative_prompt=negative_prompt,
            style_preset=style_preset,
            seed=seed
        )
    
    def check_job_status(self, job_id: str) -> Dict:
        """Check the status of a video generation job"""
        return self.ai_client.check_video_job_status(job_id)
    
    def wait_for_video_completion(self, job_id: str, max_wait_time: int = None) -> Dict:
        """
        Wait for video generation to complete
        
        Args:
            job_id: The job ID to check
            max_wait_time: Maximum time to wait in seconds (defaults to config value)
            
        Returns:
            Dict with job status and details
        """
        if max_wait_time is None:
            max_wait_time = config.VIDEO_MAX_WAIT_TIME
            
        start_time = time.time()
        poll_interval = config.VIDEO_POLL_INTERVAL
        
        while True:
            # Check if we've exceeded the maximum wait time
            if time.time() - start_time > max_wait_time:
                return {
                    "status": "TIMEOUT",
                    "message": f"Video generation did not complete within {max_wait_time} seconds"
                }
            
            # Check job status
            status_response = self.check_job_status(job_id)
            current_status = status_response.get("status")
            print(status_response)
            
            # If completed or failed, return the status
            if current_status in ["Completed", "Failed"]:
                return status_response
                
            # Wait before checking again
            time.sleep(poll_interval)
    
    def get_video_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for accessing the video
        
        Args:
            bucket: S3 bucket name
            key: S3 object key
            expiration: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            Presigned URL for the video
        """
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expiration
        )
