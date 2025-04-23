# NovaPowered-GenAI: Amazon Bedrock and Amazon Nova Demo Application

![Amazon Bedrock](https://img.shields.io/badge/Amazon-Bedrock-orange)
![Amazon Nova](https://img.shields.io/badge/Amazon-Nova-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.2.7-green)

This is a demo application showcasing the capabilities of Amazon Bedrock and Amazon Nova models through a Streamlit interface. The application integrates various AI features including text generation, image analysis, image generation, and video generation.

## Key Features

- **Text Generation**: Leverage Amazon Nova to create high-quality text content
- **Image Analysis**: Recognize and analyze image content
- **Image Generation**: Create images from text descriptions
- **Video Generation**: Generate videos from text descriptions
- **Writing Assistant**: Get professional writing support

## Project Structure

```
NovaPowered-GenAI/
├── app.py                  # Application entry point
├── NovaPoweredApp.py       # Main application class
├── config.py               # Application configuration
├── requirements.txt        # Required libraries
├── core/                   # Core services
│   └── services/           # AI services
├── infrastructure/         # AWS connections
│   └── ai/                 # Bedrock client
├── models/                 # Model definitions
├── ui/                     # User interface components
└── utils/                  # Utilities
```

## System Requirements

- Python 3.8+
- AWS account with Amazon Bedrock access
- AWS CLI configuration

## Installation

### 1. Install Python and Set Up Virtual Environment

```bash
# Install Python (if not already installed)
# Reference: https://docs.python-guide.org/starting/install3/linux/

# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Linux/Mac
# or
myenv\Scripts\activate     # On Windows
```

### 2. Install and Configure AWS CLI

```bash
# Install AWS CLI
pip install awscli

# Configure AWS CLI
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region, and Output Format
```

### 3. Download Source Code and Install Dependencies

```bash
# Clone repository
git clone https://github.com/nguyendinhthi0705/NovaPowered-GenAI.git

# Navigate to project directory
cd NovaPowered-GenAI

# Install required libraries
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Run the application with Streamlit
streamlit run app.py --server.port 8080
```

After running the command above, the application will start and can be accessed through a web browser at: http://localhost:8080

## Using the Application

1. **Home**: Introduction to the application and its features
2. **Image Analysis**: Upload images for analysis
3. **Image Generation**: Enter descriptions to generate images
4. **Video Generation**: Enter descriptions to generate videos
5. **Writing**: Enter requirements to generate text content

## References

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Amazon Nova](https://aws.amazon.com/ai/generative-ai/nova/)
- [Amazon Nova Technical Documentation](https://assets.amazon.science/b0/2b/e74dd4f84f188701fd06792670e7/the-amazon-nova-family-of-models-technical-report-and-model-card.pdf)
- [Prompt Design Guidelines](https://aws.amazon.com/ai/generative-ai/nova)

## Contributing

Contributions are welcome! Please create an issue or pull request to improve the project.

## License

This project is distributed under the MIT license.
