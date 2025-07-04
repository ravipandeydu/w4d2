# Code Quality and Maintainability Enhancements

This document provides suggestions to enhance the Document Analyzer MCP Server's code quality, maintainability, and production readiness.

## 🏗️ Architecture Improvements

### 1. Configuration Management
**Current State**: Hard-coded configuration values scattered throughout the code.

**Enhancement**: Create a centralized configuration system:

```python
# config.py
from dataclasses import dataclass
from typing import Set, Dict, Any
import os

@dataclass
class AnalysisConfig:
    max_keywords: int = 10
    min_word_length: int = 2
    confidence_threshold: float = 0.5
    max_document_size: int = 1_000_000  # 1MB
    
@dataclass
class ServerConfig:
    name: str = "document-analyzer"
    version: str = "1.0.0"
    max_documents: int = 1000
    enable_logging: bool = True
    log_level: str = "INFO"

class Config:
    def __init__(self):
        self.analysis = AnalysisConfig()
        self.server = ServerConfig()
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        if max_keywords := os.getenv('MAX_KEYWORDS'):
            self.analysis.max_keywords = int(max_keywords)
        # Add more environment variable loading...
```

### 2. Dependency Injection
**Current State**: Direct instantiation of dependencies.

**Enhancement**: Use dependency injection for better testability:

```python
from abc import ABC, abstractmethod

class SentimentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        pass

class KeywordBasedSentimentAnalyzer(SentimentAnalyzer):
    def __init__(self, positive_words: Set[str], negative_words: Set[str]):
        self.positive_words = positive_words
        self.negative_words = negative_words
    
    def analyze(self, text: str) -> Dict[str, Any]:
        # Implementation here
        pass

class DocumentAnalyzer:
    def __init__(self, sentiment_analyzer: SentimentAnalyzer, config: Config):
        self.sentiment_analyzer = sentiment_analyzer
        self.config = config
```

## 🧪 Testing Improvements

### 1. Unit Tests
**Current State**: Basic functional testing only.

**Enhancement**: Comprehensive unit test suite:

```python
# tests/test_sentiment_analyzer.py
import pytest
from unittest.mock import Mock
from analyzer import KeywordBasedSentimentAnalyzer

class TestSentimentAnalyzer:
    @pytest.fixture
    def analyzer(self):
        positive_words = {'good', 'great', 'excellent'}
        negative_words = {'bad', 'terrible', 'awful'}
        return KeywordBasedSentimentAnalyzer(positive_words, negative_words)
    
    def test_positive_sentiment(self, analyzer):
        result = analyzer.analyze("This is great and excellent!")
        assert result['sentiment'] == 'positive'
        assert result['confidence'] > 0.5
    
    def test_negative_sentiment(self, analyzer):
        result = analyzer.analyze("This is terrible and awful!")
        assert result['sentiment'] == 'negative'
        assert result['confidence'] > 0.5
    
    def test_neutral_sentiment(self, analyzer):
        result = analyzer.analyze("The weather is cloudy today.")
        assert result['sentiment'] == 'neutral'
```

### 2. Integration Tests
```python
# tests/test_mcp_integration.py
import pytest
import asyncio
from mcp.server.stdio import stdio_server
from server import server

class TestMCPIntegration:
    @pytest.mark.asyncio
    async def test_analyze_document_tool(self):
        # Test MCP tool integration
        result = await server.call_tool(
            "analyze_document", 
            {"document_id": "doc1"}
        )
        assert result is not None
        # Add more assertions
```

## 🔒 Security Enhancements

### 1. Input Validation
**Current State**: Basic parameter checking.

**Enhancement**: Comprehensive input validation:

```python
from pydantic import BaseModel, validator, Field
from typing import Optional

class DocumentData(BaseModel):
    id: str = Field(..., min_length=1, max_length=50, regex=r'^[a-zA-Z0-9_-]+$')
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=1_000_000)
    category: Optional[str] = Field(None, max_length=50)
    author: Optional[str] = Field(None, max_length=100)
    date: Optional[str] = Field(None, regex=r'^\d{4}-\d{2}-\d{2}$')
    
    @validator('content')
    def validate_content(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Content cannot be empty or whitespace only')
        return v

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    
    @validator('query')
    def sanitize_query(cls, v):
        # Remove potentially harmful characters
        import re
        return re.sub(r'[<>"\';]', '', v)
```

### 2. Rate Limiting
```python
from collections import defaultdict
from time import time
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        now = time()
        client_requests = self.requests[client_id]
        
        # Remove old requests outside the window
        client_requests[:] = [req_time for req_time in client_requests 
                             if now - req_time < self.window_seconds]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True
```

## 📊 Monitoring and Observability

### 1. Structured Logging
**Current State**: No logging system.

**Enhancement**: Comprehensive logging:

```python
import logging
import json
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_tool_call(self, tool_name: str, args: Dict[str, Any], 
                     execution_time: float, success: bool):
        log_data = {
            "event": "tool_call",
            "tool_name": tool_name,
            "args": args,
            "execution_time_ms": execution_time * 1000,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if success:
            self.logger.info(json.dumps(log_data))
        else:
            self.logger.error(json.dumps(log_data))
```

### 2. Metrics Collection
```python
from collections import Counter, defaultdict
from time import time
from typing import Dict, List

class MetricsCollector:
    def __init__(self):
        self.tool_calls = Counter()
        self.execution_times: Dict[str, List[float]] = defaultdict(list)
        self.error_counts = Counter()
        self.start_time = time()
    
    def record_tool_call(self, tool_name: str, execution_time: float, 
                        success: bool):
        self.tool_calls[tool_name] += 1
        self.execution_times[tool_name].append(execution_time)
        
        if not success:
            self.error_counts[tool_name] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        uptime = time() - self.start_time
        
        avg_times = {}
        for tool, times in self.execution_times.items():
            avg_times[tool] = sum(times) / len(times) if times else 0
        
        return {
            "uptime_seconds": uptime,
            "total_tool_calls": sum(self.tool_calls.values()),
            "tool_call_counts": dict(self.tool_calls),
            "average_execution_times": avg_times,
            "error_counts": dict(self.error_counts)
        }
```

## 🚀 Performance Optimizations

### 1. Caching
**Current State**: No caching mechanism.

**Enhancement**: Intelligent caching system:

```python
from functools import lru_cache
from typing import Tuple, Dict, Any
import hashlib

class AnalysisCache:
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def _get_cache_key(self, text: str, analysis_type: str) -> str:
        """Generate cache key from text and analysis type"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{analysis_type}:{text_hash}"
    
    def get(self, text: str, analysis_type: str) -> Optional[Dict[str, Any]]:
        key = self._get_cache_key(text, analysis_type)
        return self._cache.get(key)
    
    def set(self, text: str, analysis_type: str, result: Dict[str, Any]):
        if len(self._cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        key = self._get_cache_key(text, analysis_type)
        self._cache[key] = result

# Usage in DocumentAnalyzer
class DocumentAnalyzer:
    def __init__(self, cache: AnalysisCache):
        self.cache = cache
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        # Check cache first
        cached_result = self.cache.get(text, "sentiment")
        if cached_result:
            return cached_result
        
        # Perform analysis
        result = self._perform_sentiment_analysis(text)
        
        # Cache result
        self.cache.set(text, "sentiment", result)
        return result
```

### 2. Async Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

class AsyncDocumentAnalyzer:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def analyze_documents_batch(self, 
                                    document_ids: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple documents concurrently"""
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(
                self.executor, 
                self._analyze_single_document, 
                doc_id
            )
            for doc_id in document_ids
        ]
        
        return await asyncio.gather(*tasks)
```

## 📁 Code Organization

### 1. Modular Structure
**Current State**: Single large file.

**Enhancement**: Organized module structure:

```
document_analyzer/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── sentiment.py
│   ├── keywords.py
│   └── readability.py
├── storage/
│   ├── __init__.py
│   ├── document_store.py
│   └── sample_data.py
├── server/
│   ├── __init__.py
│   ├── mcp_server.py
│   └── handlers.py
├── utils/
│   ├── __init__.py
│   ├── validation.py
│   ├── caching.py
│   └── metrics.py
└── tests/
    ├── __init__.py
    ├── test_analyzer.py
    ├── test_sentiment.py
    └── test_server.py
```

### 2. Error Handling
**Current State**: Basic error handling.

**Enhancement**: Comprehensive error handling:

```python
class DocumentAnalyzerError(Exception):
    """Base exception for document analyzer"""
    pass

class DocumentNotFoundError(DocumentAnalyzerError):
    """Raised when document is not found"""
    pass

class InvalidDocumentError(DocumentAnalyzerError):
    """Raised when document data is invalid"""
    pass

class AnalysisError(DocumentAnalyzerError):
    """Raised when analysis fails"""
    pass

# Usage in handlers
async def handle_analyze_document(document_id: str) -> Dict[str, Any]:
    try:
        if not document_id:
            raise InvalidDocumentError("Document ID cannot be empty")
        
        document = get_document(document_id)
        if not document:
            raise DocumentNotFoundError(f"Document '{document_id}' not found")
        
        return perform_analysis(document)
        
    except DocumentAnalyzerError as e:
        logger.error(f"Analysis error: {e}")
        return {"error": str(e), "type": type(e).__name__}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": "Internal server error", "type": "UnexpectedError"}
```

## 🔧 Development Tools

### 1. Code Quality Tools
Add to `requirements-dev.txt`:
```
# Code formatting
black>=23.0.0
isort>=5.12.0

# Linting
flake8>=6.0.0
mypy>=1.0.0
pylint>=2.17.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0

# Security
bandit>=1.7.0
safety>=2.3.0
```

### 2. Pre-commit Hooks
Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

### 3. CI/CD Pipeline
Create `.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=document_analyzer --cov-report=xml
    
    - name: Run linting
      run: |
        flake8 document_analyzer/
        mypy document_analyzer/
        bandit -r document_analyzer/
```

## 📈 Scalability Considerations

### 1. Database Integration
**Current State**: In-memory document storage.

**Enhancement**: Persistent storage with database:

```python
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50))
    author = Column(String(100))
    created_date = Column(DateTime)
    
class DatabaseDocumentStore:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_document(self, document_id: str) -> Optional[Document]:
        return self.session.query(Document).filter(
            Document.id == document_id
        ).first()
    
    def search_documents(self, query: str) -> List[Document]:
        return self.session.query(Document).filter(
            Document.content.contains(query) |
            Document.title.contains(query)
        ).all()
```

### 2. Microservices Architecture
```python
# Separate analysis services
class SentimentService:
    async def analyze(self, text: str) -> Dict[str, Any]:
        # Could be a separate microservice
        pass

class KeywordService:
    async def extract(self, text: str, limit: int) -> List[str]:
        # Could be a separate microservice
        pass

class ReadabilityService:
    async def calculate(self, text: str) -> Dict[str, Any]:
        # Could be a separate microservice
        pass
```

## 🎯 Implementation Priority

### High Priority (Immediate)
1. **Error Handling**: Implement comprehensive error handling
2. **Input Validation**: Add Pydantic models for validation
3. **Logging**: Add structured logging
4. **Unit Tests**: Create basic unit test suite

### Medium Priority (Next Sprint)
1. **Configuration Management**: Centralize configuration
2. **Caching**: Implement analysis result caching
3. **Code Organization**: Split into modules
4. **Documentation**: Add inline documentation

### Low Priority (Future)
1. **Database Integration**: Replace in-memory storage
2. **Microservices**: Split into separate services
3. **Advanced Analytics**: Add more sophisticated analysis
4. **Performance Optimization**: Implement async processing

These enhancements will significantly improve the code quality, maintainability, and production readiness of the Document Analyzer MCP Server.