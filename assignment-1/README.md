# Document Analyzer MCP Server

A Model Context Protocol (MCP) server that provides comprehensive text document analysis capabilities including sentiment analysis, keyword extraction, readability scoring, and basic text statistics.

## Features

### Document Storage
- Pre-loaded with 16 sample documents across various categories
- Support for adding new documents with metadata
- Document search functionality

### Analysis Capabilities
- **Sentiment Analysis**: Determines if text is positive, negative, or neutral with confidence scores
- **Keyword Extraction**: Identifies the most important terms in documents
- **Readability Scoring**: Calculates Flesch Reading Ease scores and reading levels
- **Basic Statistics**: Word count, sentence count, paragraph count, and character counts

## MCP Tools

The server implements the following MCP tools:

### 1. `analyze_document(document_id)`
Performs comprehensive analysis of a stored document including:
- Document metadata (title, author, category, date)
- Sentiment analysis
- Top 10 keywords
- Readability metrics
- Basic text statistics

**Parameters:**
- `document_id` (string): ID of the document to analyze

### 2. `get_sentiment(text)`
Analyzes sentiment of any provided text.

**Parameters:**
- `text` (string): Text to analyze for sentiment

**Returns:**
- Sentiment classification (positive/negative/neutral)
- Confidence score
- Count of positive and negative words

### 3. `extract_keywords(text, limit)`
Extracts top keywords from provided text.

**Parameters:**
- `text` (string): Text to extract keywords from
- `limit` (integer, optional): Maximum number of keywords to return (default: 10)

### 4. `add_document(document_data)`
Adds a new document to the collection.

**Parameters:**
- `document_data` (object): Document information including:
  - `id` (string, required): Unique document identifier
  - `title` (string, required): Document title
  - `content` (string, required): Document content
  - `category` (string, optional): Document category
  - `author` (string, optional): Document author
  - `date` (string, optional): Document date (auto-generated if not provided)

### 5. `search_documents(query)`
Searches documents by content or metadata.

**Parameters:**
- `query` (string): Search query to find documents

**Returns:**
- List of matching documents with metadata and content previews
- Total number of matches

## Sample Documents

The server comes pre-loaded with 16 diverse sample documents:

1. **Product Review** - Smartphone review (positive sentiment)
2. **Technical Documentation** - API guide (neutral)
3. **Customer Complaint** - Service issue (negative sentiment)
4. **News Article** - Climate change report
5. **Blog Post** - Travel experience
6. **Academic Paper** - Machine learning research
7. **Product Manual** - Coffee machine instructions
8. **Meeting Minutes** - Project planning notes
9. **Email** - Marketing campaign results
10. **Report** - Sales performance analysis
11. **Story** - Short fiction piece
12. **Recipe** - Chocolate cake instructions
13. **Policy Document** - Remote work policy
14. **Tutorial** - Web development guide
15. **Press Release** - Product launch announcement
16. **Survey Results** - Customer feedback analysis

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the MCP server:
```bash
python server.py
```

## Usage Examples

### Analyze a Document
```json
{
  "tool": "analyze_document",
  "arguments": {
    "document_id": "doc1"
  }
}
```

### Get Sentiment of Text
```json
{
  "tool": "get_sentiment",
  "arguments": {
    "text": "I love this new feature! It's absolutely amazing."
  }
}
```

### Extract Keywords
```json
{
  "tool": "extract_keywords",
  "arguments": {
    "text": "Machine learning algorithms are revolutionizing artificial intelligence applications.",
    "limit": 5
  }
}
```

### Add New Document
```json
{
  "tool": "add_document",
  "arguments": {
    "document_data": {
      "id": "doc17",
      "title": "My New Document",
      "content": "This is the content of my new document.",
      "category": "personal",
      "author": "User"
    }
  }
}
```

### Search Documents
```json
{
  "tool": "search_documents",
  "arguments": {
    "query": "machine learning"
  }
}
```

## Technical Implementation

### Sentiment Analysis
- Uses keyword-based approach with predefined positive and negative word lists
- Calculates confidence scores based on sentiment word density
- Returns sentiment classification and word counts

### Keyword Extraction
- Removes common stop words and short words
- Uses frequency analysis to identify important terms
- Returns ranked list of keywords

### Readability Analysis
- Implements Flesch Reading Ease formula
- Calculates average sentence length and syllables per word
- Provides reading level classifications from "Very Easy" to "Very Difficult"

### Text Statistics
- Word count, sentence count, paragraph count
- Character count (with and without spaces)
- Average metrics for readability assessment

## Architecture

The server is built using the Model Context Protocol (MCP) framework and consists of:

- **DocumentAnalyzer Class**: Core analysis engine
- **MCP Server**: Handles tool registration and execution
- **Sample Data**: Pre-loaded document collection
- **Analysis Methods**: Sentiment, keyword, readability, and statistics functions

## Requirements

- Python 3.8+
- MCP framework
- Standard library modules (re, json, math, collections, datetime)

This MCP server provides a comprehensive solution for document analysis tasks and can be easily integrated into larger systems requiring text analysis capabilities.