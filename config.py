# Configuration settings for the application

# AWS Region
AWS_REGION = "us-east-1"

# S3 Configuration for video output
# IMPORTANT: This must be an existing bucket with proper permissions
S3_BUCKET_NAME = "s3://my-nova-videos"  # Replace with an existing bucket you have access to
S3_OUTPUT_KEY ="output.mp4"
# Model IDs
NOVA_PRO_MODEL_ID = "amazon.nova-pro-v1:0"
NOVA_CANVAS_MODEL_ID = "amazon.nova-canvas-v1:0"
NOVA_REEL_MODEL_ID = "amazon.nova-reel-v1:0"  # Using the correct Nova Reel model ID

# Video Generation Settings
DEFAULT_VIDEO_DURATION = 5  # seconds
MAX_VIDEO_DURATION = 10  # seconds
VIDEO_POLL_INTERVAL = 5  # seconds to wait between status checks
VIDEO_MAX_WAIT_TIME = 300  # maximum seconds to wait for video generation (5 minutes)
