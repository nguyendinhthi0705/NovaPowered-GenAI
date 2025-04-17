# Phân tích và đề xuất refactor theo hướng OOP và unit test

## 1. Phân tích cấu trúc hiện tại

### 1.1 Cấu trúc thư mục
Dự án hiện tại đã có cấu trúc phân chia theo chức năng:
- `models/`: Chứa các lớp làm việc với dữ liệu và API bên ngoài
- `services/`: Chứa các lớp dịch vụ xử lý logic nghiệp vụ
- `ui/`: Chứa các lớp giao diện người dùng
- `utils/`: Chứa các tiện ích

### 1.2 Các thành phần chính
- `NovaPoweredApp`: Lớp chính điều phối ứng dụng
- `BedrockClient`: Giao tiếp với Amazon Bedrock API
- `AIService`: Cung cấp các dịch vụ AI
- `KnowledgeBaseService`: Xử lý truy vấn cơ sở kiến thức
- `BasePage` và các lớp con: Xử lý giao diện người dùng

## 2. Vấn đề trong thiết kế hiện tại

### 2.1 Thiếu tính đóng gói và trừu tượng
- Các lớp có sự phụ thuộc chặt chẽ vào nhau
- Thiếu các interface để định nghĩa hợp đồng giữa các thành phần
- Các phương thức trong `AIService` có nhiều code trùng lặp (prompt templates)

### 2.2 Khó kiểm thử
- Không có cơ chế dependency injection rõ ràng
- Thiếu các mock objects cho việc kiểm thử
- Không có cấu trúc để viết unit test

### 2.3 Thiếu tính mở rộng
- Khó thêm mới các model AI khác ngoài Amazon Bedrock
- Khó thay đổi cấu trúc prompt mà không sửa đổi code
- Khó thêm các tính năng mới

## 3. Đề xuất refactor

### 3.1 Áp dụng nguyên tắc SOLID

#### 3.1.1 Single Responsibility Principle
- Tách các lớp thành các thành phần nhỏ hơn, mỗi lớp chỉ có một trách nhiệm
- Ví dụ: Tách `AIService` thành các service nhỏ hơn theo chức năng

#### 3.1.2 Open/Closed Principle
- Thiết kế các interface để mở rộng mà không cần sửa đổi code hiện có
- Ví dụ: Interface `AIModelClient` cho phép thêm các model AI khác ngoài Bedrock

#### 3.1.3 Liskov Substitution Principle
- Đảm bảo các lớp con có thể thay thế lớp cha mà không làm thay đổi tính đúng đắn của chương trình
- Ví dụ: Các lớp con của `BasePage` cần tuân thủ hợp đồng của lớp cha

#### 3.1.4 Interface Segregation Principle
- Tạo các interface nhỏ, cụ thể thay vì một interface lớn
- Ví dụ: Tách `AIService` thành các interface nhỏ hơn như `TextGenerationService`, `ImageAnalysisService`

#### 3.1.5 Dependency Inversion Principle
- Các module cấp cao không nên phụ thuộc vào module cấp thấp, cả hai nên phụ thuộc vào abstraction
- Ví dụ: `AIService` nên phụ thuộc vào interface `AIModelClient` thay vì `BedrockClient`

### 3.2 Cấu trúc thư mục mới

```
NovaPowered-GenAI/
├── config/                  # Cấu hình ứng dụng
│   ├── __init__.py
│   └── app_config.py        # Cấu hình chung
├── models/                  # Định nghĩa dữ liệu
│   ├── __init__.py
│   └── dto/                 # Data Transfer Objects
├── core/                    # Logic nghiệp vụ cốt lõi
│   ├── __init__.py
│   ├── interfaces/          # Các interface
│   │   ├── __init__.py
│   │   ├── ai_client.py     # Interface cho AI client
│   │   └── knowledge_base.py # Interface cho Knowledge Base
│   ├── services/            # Các service
│   │   ├── __init__.py
│   │   ├── text_generation.py
│   │   ├── image_analysis.py
│   │   └── knowledge_base.py
│   └── prompt_templates/    # Các template cho prompt
│       ├── __init__.py
│       └── templates.py
├── infrastructure/          # Giao tiếp với dịch vụ bên ngoài
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── bedrock_client.py
│   │   └── image_processor.py
│   └── knowledge_base/
│       ├── __init__.py
│       └── amazon_kb_client.py
├── ui/                      # Giao diện người dùng
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   └── base_page.py
│   └── pages/
│       ├── __init__.py
│       ├── home_page.py
│       ├── image_analysis_page.py
│       └── ...
├── utils/                   # Tiện ích
│   ├── __init__.py
│   └── helpers.py
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_ai_service.py
│   │   └── ...
│   └── integration/
│       ├── __init__.py
│       └── ...
├── app.py                   # Entry point
└── requirements.txt
```

## 4. Chi tiết refactor

### 4.1 Interfaces

#### 4.1.1 AIClient Interface
```python
from abc import ABC, abstractmethod
from typing import Generator, Optional

class AIClient(ABC):
    """Interface for AI model clients"""
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generate text from prompt"""
        pass
        
    @abstractmethod
    def generate_text_stream(self, prompt: str) -> Generator[str, None, None]:
        """Generate text from prompt with streaming response"""
        pass
        
    @abstractmethod
    def analyze_image(self, prompt: str, image_bytes: bytes) -> str:
        """Analyze image with prompt"""
        pass
        
    @abstractmethod
    def analyze_image_stream(self, prompt: str, image_bytes: bytes) -> Generator[str, None, None]:
        """Analyze image with prompt with streaming response"""
        pass
```

#### 4.1.2 KnowledgeBase Interface
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Generator

class KnowledgeBase(ABC):
    """Interface for knowledge base operations"""
    
    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search knowledge base"""
        pass
        
    @abstractmethod
    def search_and_generate(self, query: str) -> Generator[str, None, None]:
        """Search knowledge base and generate response"""
        pass
```

### 4.2 Implementations

#### 4.2.1 BedrockClient Implementation
```python
import json
import boto3
from typing import Dict, Generator, Optional
from core.interfaces.ai_client import AIClient
from infrastructure.ai.image_processor import ImageProcessor

class BedrockClient(AIClient):
    """Implementation of AIClient using Amazon Bedrock"""
    
    def __init__(self, model_id: str = "amazon.nova-pro-v1:0", region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id
        self.image_processor = ImageProcessor()
    
    def _create_request_body(self, prompt: str, image_bytes: Optional[bytes] = None, 
                           inference_params: Optional[Dict] = None) -> str:
        """Create request body for Bedrock API"""
        # Implementation...
        
    def generate_text(self, prompt: str) -> str:
        """Generate text from prompt"""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=self._create_request_body(prompt)
        )
        # Process response and return text
        
    def generate_text_stream(self, prompt: str) -> Generator[str, None, None]:
        """Generate text from prompt with streaming response"""
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=self._create_request_body(prompt)
        )
        # Process streaming response and yield text chunks
        
    def analyze_image(self, prompt: str, image_bytes: bytes) -> str:
        """Analyze image with prompt"""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=self._create_request_body(prompt, image_bytes)
        )
        # Process response and return text
        
    def analyze_image_stream(self, prompt: str, image_bytes: bytes) -> Generator[str, None, None]:
        """Analyze image with prompt with streaming response"""
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=self._create_request_body(prompt, image_bytes)
        )
        # Process streaming response and yield text chunks
```

### 4.3 Services

#### 4.3.1 TextGenerationService
```python
from typing import Generator, Dict
from core.interfaces.ai_client import AIClient
from core.prompt_templates.templates import PromptTemplates

class TextGenerationService:
    """Service for text generation operations"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.templates = PromptTemplates()
    
    def rewrite_document(self, input_text: str) -> Generator[str, None, None]:
        """Rewrite document with stronger words"""
        prompt = self.templates.get_template("rewrite").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def summarize(self, input_text: str) -> Generator[str, None, None]:
        """Summarize text"""
        prompt = self.templates.get_template("summary").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def create_star_report(self, input_text: str) -> Generator[str, None, None]:
        """Create STAR format report"""
        prompt = self.templates.get_template("star_report").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
        
    def suggest_writing_improvements(self, input_text: str) -> Generator[str, None, None]:
        """Suggest improvements for writing"""
        prompt = self.templates.get_template("improve_writing").format(content=input_text)
        return self.ai_client.generate_text_stream(prompt)
```

#### 4.3.2 ImageAnalysisService
```python
from typing import Generator
from core.interfaces.ai_client import AIClient

class ImageAnalysisService:
    """Service for image analysis operations"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    def analyze_image(self, prompt: str, image_bytes: bytes) -> Generator[str, None, None]:
        """Analyze image with prompt"""
        return self.ai_client.analyze_image_stream(prompt, image_bytes)
```

### 4.4 Prompt Templates
```python
class PromptTemplates:
    """Manages prompt templates"""
    
    def __init__(self):
        self.templates = {
            "rewrite": """Your name is good writer. You need to rewrite content use stronger words to hight: 
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "summary": """Based on the provided context, create summary the lecture
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "star_report": """Your name is good writer. You need to rewrite content use stronger words to and format in STAR format: 
            \n\Content:
            <text>{content}</text>""",
            
            "improve_writing": """Your name is good writer. You need to suggest and correct mistake in the essay: 
            \n\nHuman: here is the content
            <text>{content}</text>
            \n\nAssistant: """,
            
            "query_document": """Human: here is the content:
            <text>{content}</text>
            Question: {question} 
            \n\nAssistant: """
        }
    
    def get_template(self, template_name: str) -> str:
        """Get template by name"""
        return self.templates.get(template_name, "")
        
    def add_template(self, name: str, template: str) -> None:
        """Add new template"""
        self.templates[name] = template
```

## 5. Unit Testing

### 5.1 Cấu trúc Unit Test

```python
# tests/unit/test_bedrock_client.py
import unittest
from unittest.mock import Mock, patch
from core.interfaces.ai_client import AIClient
from infrastructure.ai.bedrock_client import BedrockClient

class TestBedrockClient(unittest.TestCase):
    
    def setUp(self):
        # Setup mock boto3 client
        self.mock_boto3_client = Mock()
        with patch('boto3.client', return_value=self.mock_boto3_client):
            self.client = BedrockClient()
    
    def test_generate_text(self):
        # Setup mock response
        mock_response = {
            'body': Mock(),
            'ResponseMetadata': {'RequestId': 'test-id'}
        }
        self.mock_boto3_client.invoke_model.return_value = mock_response
        
        # Test
        result = self.client.generate_text("Test prompt")
        
        # Assert
        self.mock_boto3_client.invoke_model.assert_called_once()
        # Additional assertions...
        
    def test_analyze_image(self):
        # Similar test for image analysis
        pass
```

### 5.2 Mocking Dependencies

```python
# tests/unit/test_text_generation_service.py
import unittest
from unittest.mock import Mock
from core.services.text_generation import TextGenerationService

class TestTextGenerationService(unittest.TestCase):
    
    def setUp(self):
        self.mock_ai_client = Mock()
        self.service = TextGenerationService(self.mock_ai_client)
    
    def test_rewrite_document(self):
        # Setup
        mock_generator = (item for item in ["This", " is", " a", " test"])
        self.mock_ai_client.generate_text_stream.return_value = mock_generator
        
        # Test
        result = list(self.service.rewrite_document("Test input"))
        
        # Assert
        self.mock_ai_client.generate_text_stream.assert_called_once()
        self.assertEqual(result, ["This", " is", " a", " test"])
        
    # Additional tests...
```

## 6. Kế hoạch triển khai

### 6.1 Các bước refactor
1. Tạo các interface cần thiết
2. Refactor các implementation hiện có để implement các interface
3. Tạo các service mới với dependency injection
4. Cập nhật UI để sử dụng các service mới
5. Viết unit test cho từng thành phần

### 6.2 Lợi ích sau khi refactor
1. Code dễ bảo trì và mở rộng hơn
2. Dễ dàng thêm các model AI mới
3. Dễ dàng thay đổi prompt template mà không cần sửa code
4. Có thể kiểm thử tự động với unit test
5. Giảm sự phụ thuộc giữa các thành phần

### 6.3 Rủi ro và giảm thiểu
1. Rủi ro: Thời gian refactor có thể kéo dài
   - Giảm thiểu: Refactor từng phần nhỏ, đảm bảo tính năng vẫn hoạt động
2. Rủi ro: Có thể phát sinh lỗi mới
   - Giảm thiểu: Viết unit test trước khi refactor để đảm bảo tính năng không bị thay đổi
