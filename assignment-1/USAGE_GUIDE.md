# Document Analyzer MCP Server - Usage Guide

This guide provides step-by-step instructions on how to set up, run, and use the Document Analyzer MCP Server.

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** installed on your system
- **MCP-compatible client** (like Claude Desktop, Cline, or any MCP client)
- **Command line access** (Terminal, PowerShell, or Command Prompt)

### 2. Installation

#### Step 1: Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd assignment-1

# Or download and extract the ZIP file
```

#### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Running the Server

#### Method 1: Direct Execution
```bash
python server.py
```

#### Method 2: As MCP Server (Recommended)
The server is designed to be used with MCP-compatible clients. Configure your MCP client to connect to this server.

## 🔧 Configuration for MCP Clients

### Claude Desktop Configuration

Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["path/to/your/server.py"],
      "cwd": "path/to/your/project"
    }
  }
}
```

### Cline Configuration

In Cline, add the server configuration:

```json
{
  "name": "document-analyzer",
  "command": "python server.py",
  "cwd": "./assignment-1"
}
```

## 📚 Available Tools

The server provides 5 main tools for document analysis:

### 1. `analyze_document` - Complete Document Analysis

**Purpose**: Performs comprehensive analysis including sentiment, keywords, readability, and statistics.

**Parameters**:
- `document_id` (string): ID of the document to analyze

**Example Usage**:
```json
{
  "tool": "analyze_document",
  "arguments": {
    "document_id": "tech_article_1"
  }
}
```

**Sample Response**:
```json
{
  "document_id": "tech_article_1",
  "title": "The Future of Artificial Intelligence",
  "sentiment": {
    "sentiment": "positive",
    "confidence": 0.75,
    "positive_score": 0.75,
    "negative_score": 0.25
  },
  "keywords": ["artificial", "intelligence", "future", "technology"],
  "readability": {
    "flesch_reading_ease": 65.2,
    "flesch_kincaid_grade": 8.5,
    "difficulty": "Standard"
  },
  "statistics": {
    "word_count": 245,
    "sentence_count": 12,
    "paragraph_count": 4,
    "avg_words_per_sentence": 20.4
  }
}
```

### 2. `get_sentiment` - Sentiment Analysis Only

**Purpose**: Analyzes the emotional tone of a document.

**Parameters**:
- `document_id` (string): ID of the document to analyze

**Example Usage**:
```json
{
  "tool": "get_sentiment",
  "arguments": {
    "document_id": "news_article_1"
  }
}
```

### 3. `extract_keywords` - Keyword Extraction

**Purpose**: Extracts important keywords from a document.

**Parameters**:
- `document_id` (string): ID of the document to analyze
- `limit` (integer, optional): Maximum number of keywords to return (default: 10)

**Example Usage**:
```json
{
  "tool": "extract_keywords",
  "arguments": {
    "document_id": "research_paper_1",
    "limit": 15
  }
}
```

### 4. `add_document` - Add New Document

**Purpose**: Adds a new document to the collection for analysis.

**Parameters**:
- `document_id` (string): Unique ID for the document
- `title` (string): Document title
- `content` (string): Document content
- `category` (string, optional): Document category
- `author` (string, optional): Document author
- `date` (string, optional): Document date

**Example Usage**:
```json
{
  "tool": "add_document",
  "arguments": {
    "document_id": "my_article_1",
    "title": "My Research Findings",
    "content": "This document contains my latest research findings on machine learning algorithms...",
    "category": "research",
    "author": "John Doe",
    "date": "2024-01-15"
  }
}
```

### 5. `search_documents` - Document Search

**Purpose**: Searches for documents containing specific terms.

**Parameters**:
- `query` (string): Search terms

**Example Usage**:
```json
{
  "tool": "search_documents",
  "arguments": {
    "query": "artificial intelligence"
  }
}
```

## 📖 Pre-loaded Sample Documents

The server comes with 16 sample documents across different categories:

### Technology (4 documents)
- `tech_article_1`: "The Future of Artificial Intelligence"
- `tech_article_2`: "Blockchain Revolution"
- `tech_article_3`: "Quantum Computing Breakthrough"
- `tech_article_4`: "5G Network Implementation"

### Business (4 documents)
- `business_report_1`: "Q4 Financial Performance"
- `business_report_2`: "Market Analysis Report"
- `business_report_3`: "Strategic Planning Document"
- `business_report_4`: "Customer Satisfaction Survey"

### Science (4 documents)
- `science_paper_1`: "Climate Change Impact Study"
- `science_paper_2`: "Genetic Engineering Research"
- `science_paper_3`: "Space Exploration Mission"
- `science_paper_4`: "Renewable Energy Solutions"

### News (4 documents)
- `news_article_1`: "Global Economic Outlook"
- `news_article_2`: "Healthcare Innovation"
- `news_article_3`: "Educational Reform Initiative"
- `news_article_4`: "Environmental Conservation Efforts"

## 🎯 Common Use Cases

### 1. Content Analysis Workflow

```bash
# 1. First, search for relevant documents
search_documents("technology")

# 2. Analyze a specific document
analyze_document("tech_article_1")

# 3. Get detailed sentiment analysis
get_sentiment("tech_article_1")

# 4. Extract keywords for tagging
extract_keywords("tech_article_1", limit=20)
```

### 2. Adding and Analyzing New Content

```bash
# 1. Add your document
add_document(
  document_id="my_blog_post",
  title="My Thoughts on AI",
  content="Your blog post content here...",
  category="opinion"
)

# 2. Analyze the new document
analyze_document("my_blog_post")
```

### 3. Research and Content Discovery

```bash
# 1. Search for documents on a topic
search_documents("climate change")

# 2. Analyze sentiment across multiple documents
get_sentiment("science_paper_1")
get_sentiment("news_article_4")

# 3. Compare readability scores
analyze_document("science_paper_1")  # Check readability.flesch_reading_ease
analyze_document("news_article_4")   # Compare with this one
```

## 🔍 Understanding the Analysis Results

### Sentiment Analysis
- **sentiment**: "positive", "negative", or "neutral"
- **confidence**: 0.0 to 1.0 (higher = more confident)
- **positive_score**: Ratio of positive words
- **negative_score**: Ratio of negative words

### Readability Scores
- **flesch_reading_ease**: 0-100 (higher = easier to read)
  - 90-100: Very Easy
  - 80-90: Easy
  - 70-80: Fairly Easy
  - 60-70: Standard
  - 50-60: Fairly Difficult
  - 30-50: Difficult
  - 0-30: Very Difficult
- **flesch_kincaid_grade**: Grade level (e.g., 8.5 = 8th grade level)
- **difficulty**: Text description of reading difficulty

### Keywords
- Extracted based on word frequency and importance
- Filtered to remove common stop words
- Sorted by relevance

### Statistics
- **word_count**: Total number of words
- **sentence_count**: Total number of sentences
- **paragraph_count**: Total number of paragraphs
- **avg_words_per_sentence**: Average sentence length

## 🛠️ Testing and Verification

### Run Standalone Tests
```bash
# Test core functionality without MCP
python standalone_test.py
```

### Run Example Usage
```bash
# See example tool usage
python example_usage.py
```

### Run MCP Server Tests
```bash
# Test MCP server functionality (requires mcp package)
python test_server.py
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'mcp'"
**Solution**: Install the mcp package
```bash
pip install mcp
```

#### 2. "Document not found" error
**Solution**: Check available documents first
```bash
# Use search_documents to see available documents
search_documents("")
```

#### 3. Server not responding
**Solution**: Check if server is running and accessible
```bash
# Restart the server
python server.py
```

#### 4. Permission errors
**Solution**: Ensure proper file permissions and virtual environment activation
```bash
# Reactivate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### Debug Mode

For debugging, you can modify the server to add more logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Tips

1. **Document Size**: Keep documents under 100KB for optimal performance
2. **Batch Operations**: Use search to find multiple documents, then analyze individually
3. **Caching**: Results are not cached, so repeated analysis of the same document will recalculate
4. **Memory Usage**: The server keeps all documents in memory for fast access

## 🔗 Integration Examples

### With Claude Desktop

1. Configure the server in Claude Desktop settings
2. Use natural language to request analysis:
   - "Analyze the sentiment of tech_article_1"
   - "Extract keywords from the business report"
   - "What's the readability score of science_paper_1?"

### With Custom Applications

```python
# Example Python client code
import asyncio
from mcp.client.stdio import stdio_client

async def analyze_document_example():
    async with stdio_client(["python", "server.py"]) as client:
        result = await client.call_tool(
            "analyze_document", 
            {"document_id": "tech_article_1"}
        )
        print(result)

asyncio.run(analyze_document_example())
```

## 📝 Best Practices

1. **Document IDs**: Use descriptive, unique IDs for your documents
2. **Categories**: Organize documents with consistent category names
3. **Content Quality**: Ensure documents have sufficient content for meaningful analysis
4. **Regular Testing**: Test your setup with the provided test scripts
5. **Error Handling**: Always check for errors in tool responses

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Run the test scripts to verify functionality
3. Review the server logs for error messages
4. Ensure all dependencies are properly installed
5. Verify your MCP client configuration

The Document Analyzer MCP Server is designed to be robust and user-friendly. With this guide, you should be able to set up and use all its features effectively!