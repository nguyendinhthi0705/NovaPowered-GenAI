# Refactoring NovaPowered-GenAI to OOP Architecture

## Current Structure Analysis

The current application is structured as follows:

- **Home.py**: Main entry point with simple UI
- **Libs.py**: Contains all utility functions and API calls
- **pages/**: Multiple Streamlit pages for different functionalities
  - 0_Analyze_Image.py
  - 1_Analyze_Document.py
  - 2_STAR_Report.py
  - 3_Improve_Writing.py
  - 4_Rewrite_Essay.py
  - 5_Search.py

### Issues with Current Structure

1. **Procedural Programming**: All functionality is implemented as standalone functions
2. **Code Duplication**: Similar UI patterns repeated across pages
3. **Tight Coupling**: Direct dependencies between UI and business logic
4. **Limited Extensibility**: Difficult to add new models or features
5. **No Separation of Concerns**: UI, business logic, and API calls mixed together

## Proposed OOP Architecture

### 1. Core Classes

```python
# models/bedrock_client.py
class BedrockClient:
    """Handles communication with Amazon Bedrock"""
    
    def __init__(self, region="us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = "amazon.nova-pro-v1:0"
    
    def create_request_body(self, prompt, image_bytes=None, inference_params=None):
        """Create request body for Bedrock API"""
        # Implementation here
        
    def invoke_model_stream(self, prompt, image_bytes=None, inference_params=None):
        """Invoke model with streaming response"""
        # Implementation here
```

```python
# models/image_processor.py
class ImageProcessor:
    """Handles image processing operations"""
    
    @staticmethod
    def get_bytesio_from_bytes(image_bytes):
        """Convert bytes to BytesIO object"""
        # Implementation here
        
    @staticmethod
    def get_base64_from_bytes(image_bytes):
        """Convert bytes to base64 string"""
        # Implementation here
        
    @staticmethod
    def get_bytes_from_file(file_path):
        """Read bytes from file"""
        # Implementation here
```

```python
# services/ai_service.py
class AIService:
    """Service for AI-related operations"""
    
    def __init__(self, bedrock_client=None):
        self.bedrock_client = bedrock_client or BedrockClient()
        self.image_processor = ImageProcessor()
    
    def call_stream(self, prompt, image=None):
        """Call Bedrock API with streaming response"""
        # Implementation here
        
    def rewrite_document(self, input_text):
        """Rewrite document with stronger words"""
        # Implementation here
        
    def summary_stream(self, input_text):
        """Summarize lecture"""
        # Implementation here
        
    def query_document(self, question, docs):
        """Query document with question"""
        # Implementation here
        
    def create_STAR_Report(self, input_text):
        """Create STAR report"""
        # Implementation here
        
    def suggest_writing_document(self, input_text):
        """Suggest improvements for writing"""
        # Implementation here
```

```python
# services/knowledge_base_service.py
class KnowledgeBaseService:
    """Service for knowledge base operations"""
    
    def __init__(self, knowledge_base_id="KS3NLF2KU6"):
        self.knowledge_base_id = knowledge_base_id
        
    def search(self, prompt):
        """Search knowledge base"""
        # Implementation here
```

### 2. UI Components

```python
# ui/base_page.py
class BasePage:
    """Base class for all pages"""
    
    def __init__(self, title, ai_service=None):
        self.title = title
        self.ai_service = ai_service or AIService()
        
    def setup(self):
        """Setup page configuration"""
        st.set_page_config(page_title=self.title)
        
    def render(self):
        """Render page content"""
        raise NotImplementedError("Subclasses must implement render()")
```

```python
# ui/home_page.py
class HomePage(BasePage):
    """Home page"""
    
    def render(self):
        """Render home page"""
        st.markdown("Create 1 Data-Driven Test Function with Katalon")
        # Rest of implementation
```

```python
# ui/image_analysis_page.py
class ImageAnalysisPage(BasePage):
    """Image analysis page"""
    
    def render(self):
        """Render image analysis page"""
        # Implementation here
```

### 3. Application Structure

```python
# app.py
class NovaPoweredApp:
    """Main application class"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.kb_service = KnowledgeBaseService()
        
    def run(self):
        """Run the application"""
        # Implementation here
```

## Implementation Plan

1. **Create Directory Structure**:
   ```
   NovaPowered-GenAI/
   ├── app.py
   ├── config.py
   ├── models/
   │   ├── __init__.py
   │   ├── bedrock_client.py
   │   └── image_processor.py
   ├── services/
   │   ├── __init__.py
   │   ├── ai_service.py
   │   └── knowledge_base_service.py
   ├── ui/
   │   ├── __init__.py
   │   ├── base_page.py
   │   ├── home_page.py
   │   ├── image_analysis_page.py
   │   └── ... (other pages)
   └── utils/
       ├── __init__.py
       └── helpers.py
   ```

2. **Refactor Core Functionality**:
   - Move image processing functions to `ImageProcessor` class
   - Move Bedrock API calls to `BedrockClient` class
   - Move AI operations to `AIService` class
   - Move knowledge base operations to `KnowledgeBaseService` class

3. **Refactor UI**:
   - Create base page class with common functionality
   - Create specific page classes for each feature
   - Implement consistent UI patterns

4. **Update Entry Points**:
   - Update Home.py to use new classes
   - Update page files to use new classes

## Benefits of OOP Refactoring

1. **Improved Maintainability**: Classes with single responsibilities
2. **Better Testability**: Easier to write unit tests for isolated components
3. **Enhanced Extensibility**: Easy to add new features or models
4. **Code Reusability**: Common functionality in base classes
5. **Separation of Concerns**: UI separated from business logic and API calls
6. **Dependency Injection**: Services can be mocked for testing

## Example Implementation: BedrockClient

```python
import boto3
import json
import base64
from io import BytesIO

class BedrockClient:
    def __init__(self, region="us-east-1", model_id="amazon.nova-pro-v1:0"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id
        
    def create_request_body(self, prompt, image_bytes=None, 
                           inference_params=None):
        """Create request body for Bedrock API"""
        if inference_params is None:
            inference_params = {
                "max_new_tokens": 5000, 
                "top_p": 0.1, 
                "top_k": 20, 
                "temperature": 0.3
            }
            
        if image_bytes:
            input_image_base64 = self._get_base64_from_bytes(image_bytes)
            message_list = [
                {   
                    "role": "user", 
                    "content": [                
                        {
                            "image":{
                                "format" : "jpeg" ,
                                "source":{
                                    "bytes": input_image_base64
                                }
                            }
                        },
                         {"text": prompt},
                        ]
                }]
        else:
            message_list = [{"role": "user", "content": [{"text": prompt}]}]
       
        system_list = [
                {
                    "text": "Act as a chatbot assistant. You answer the question they input in the same input languages"
                }
        ]
        
        request_body = {
            "schemaVersion": "messages-v1",
            "messages": message_list,
            "system": system_list,
            "inferenceConfig": inference_params,
        }
        return json.dumps(request_body)
    
    def invoke_model_stream(self, prompt, image_bytes=None, 
                           inference_params=None):
        """Invoke model with streaming response"""
        body = self.create_request_body(prompt, image_bytes, inference_params)
        
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id, 
            body=body
        )
        
        request_id = response.get("ResponseMetadata").get("RequestId")
        print(f"Request ID: {request_id}")
        
        stream = response.get("body")
        if not stream:
            print("No response stream received.")
            return
            
        for event in stream:
            chunk = event.get("chunk")
            if chunk:
                chunk_json = json.loads(chunk.get("bytes").decode())
                content_block_delta = chunk_json.get("contentBlockDelta")
                if content_block_delta:
                    yield content_block_delta.get("delta").get("text")
    
    def _get_bytesio_from_bytes(self, image_bytes):
        """Convert bytes to BytesIO object"""
        return BytesIO(image_bytes)
    
    def _get_base64_from_bytes(self, image_bytes):
        """Convert bytes to base64 string"""
        resized_io = self._get_bytesio_from_bytes(image_bytes)
        img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
        return img_str
```

## Next Steps

1. Create the directory structure
2. Implement core classes one by one
3. Refactor UI components
4. Update entry points
5. Test the application
6. Document the new architecture
