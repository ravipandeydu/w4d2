#!/usr/bin/env python3
"""
Example usage of Document Analyzer MCP Server
Demonstrates how to use each MCP tool with sample requests and responses.
"""

import json

def show_example_usage():
    """Display example usage of all MCP tools"""
    
    print("=" * 70)
    print("DOCUMENT ANALYZER MCP SERVER - EXAMPLE USAGE")
    print("=" * 70)
    
    # Example 1: analyze_document
    print("\n1. ANALYZE_DOCUMENT TOOL")
    print("-" * 30)
    print("Purpose: Perform full analysis of a stored document")
    print("\nExample Request:")
    request1 = {
        "tool": "analyze_document",
        "arguments": {
            "document_id": "doc1"
        }
    }
    print(json.dumps(request1, indent=2))
    
    print("\nExample Response:")
    response1 = {
        "document_info": {
            "id": "doc1",
            "title": "Product Review - Smartphone",
            "category": "review",
            "author": "John Smith",
            "date": "2024-01-15"
        },
        "sentiment_analysis": {
            "sentiment": "positive",
            "confidence": 0.75,
            "positive_words": 6,
            "negative_words": 0
        },
        "keywords": ["smartphone", "camera", "quality", "excellent", "battery"],
        "readability": {
            "flesch_score": 65.2,
            "reading_level": "Standard",
            "avg_sentence_length": 15.3,
            "avg_syllables_per_word": 1.8
        },
        "basic_stats": {
            "word_count": 46,
            "sentence_count": 3,
            "paragraph_count": 1,
            "character_count": 267,
            "character_count_no_spaces": 221
        }
    }
    print(json.dumps(response1, indent=2))
    
    # Example 2: get_sentiment
    print("\n\n2. GET_SENTIMENT TOOL")
    print("-" * 25)
    print("Purpose: Analyze sentiment of any text")
    print("\nExample Request:")
    request2 = {
        "tool": "get_sentiment",
        "arguments": {
            "text": "I love this new feature! It's absolutely amazing and works perfectly."
        }
    }
    print(json.dumps(request2, indent=2))
    
    print("\nExample Response:")
    response2 = {
        "sentiment": "positive",
        "confidence": 0.82,
        "positive_words": 4,
        "negative_words": 0
    }
    print(json.dumps(response2, indent=2))
    
    # Example 3: extract_keywords
    print("\n\n3. EXTRACT_KEYWORDS TOOL")
    print("-" * 28)
    print("Purpose: Extract top keywords from text")
    print("\nExample Request:")
    request3 = {
        "tool": "extract_keywords",
        "arguments": {
            "text": "Machine learning algorithms are revolutionizing artificial intelligence applications in modern technology sectors.",
            "limit": 5
        }
    }
    print(json.dumps(request3, indent=2))
    
    print("\nExample Response:")
    response3 = {
        "keywords": ["machine", "learning", "algorithms", "artificial", "intelligence"]
    }
    print(json.dumps(response3, indent=2))
    
    # Example 4: add_document
    print("\n\n4. ADD_DOCUMENT TOOL")
    print("-" * 22)
    print("Purpose: Add a new document to the collection")
    print("\nExample Request:")
    request4 = {
        "tool": "add_document",
        "arguments": {
            "document_data": {
                "id": "doc17",
                "title": "User Manual - Smart Watch",
                "content": "This smart watch features heart rate monitoring, GPS tracking, and waterproof design. Battery life lasts up to 7 days with normal usage.",
                "category": "manual",
                "author": "Product Team",
                "date": "2024-02-10"
            }
        }
    }
    print(json.dumps(request4, indent=2))
    
    print("\nExample Response:")
    print('"Document \'doc17\' added successfully."')
    
    # Example 5: search_documents
    print("\n\n5. SEARCH_DOCUMENTS TOOL")
    print("-" * 27)
    print("Purpose: Search documents by content or metadata")
    print("\nExample Request:")
    request5 = {
        "tool": "search_documents",
        "arguments": {
            "query": "machine learning"
        }
    }
    print(json.dumps(request5, indent=2))
    
    print("\nExample Response:")
    response5 = {
        "query": "machine learning",
        "total_matches": 1,
        "documents": [
            {
                "id": "doc6",
                "title": "Academic Paper - Machine Learning",
                "category": "academic",
                "author": "Dr. Research",
                "date": "2024-01-03",
                "content_preview": "This paper presents a novel approach to neural network optimization. The proposed algorithm demonstrates superior performance compared to existing methods..."
            }
        ]
    }
    print(json.dumps(response5, indent=2))
    
    # Usage Tips
    print("\n\n" + "=" * 70)
    print("USAGE TIPS")
    print("=" * 70)
    print("\n1. Document IDs: Use 'doc1' through 'doc16' for pre-loaded documents")
    print("2. Sentiment Analysis: Returns positive/negative/neutral with confidence scores")
    print("3. Keywords: Automatically filters out stop words and short terms")
    print("4. Readability: Uses Flesch Reading Ease formula (0-100 scale)")
    print("5. Search: Searches across title, content, category, and author fields")
    print("6. New Documents: Ensure unique IDs when adding documents")
    print("7. Text Length: No strict limits, but very long texts may affect performance")
    
    # Available Document Categories
    print("\n\nAVAILABLE DOCUMENT CATEGORIES:")
    print("-" * 35)
    categories = [
        "review", "technical", "complaint", "news", "blog", "academic",
        "manual", "meeting", "email", "report", "fiction", "recipe",
        "policy", "tutorial", "press", "survey"
    ]
    for i, category in enumerate(categories, 1):
        print(f"{i:2d}. {category}")
    
    print("\n" + "=" * 70)
    print("Ready to use with any MCP-compatible client!")
    print("=" * 70)

if __name__ == "__main__":
    show_example_usage()