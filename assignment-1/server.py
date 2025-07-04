#!/usr/bin/env python3
"""
Document Analyzer MCP Server
Provides text analysis capabilities including sentiment analysis, keyword extraction, and readability scoring.
"""

import asyncio
import json
import re
import math
from collections import Counter
from typing import Any, Dict, List, Optional
from datetime import datetime

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

# Simple sentiment analysis using keyword-based approach
POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome',
    'love', 'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'delighted',
    'perfect', 'brilliant', 'outstanding', 'superb', 'magnificent', 'beautiful',
    'positive', 'optimistic', 'cheerful', 'joyful', 'excited', 'thrilled'
}

NEGATIVE_WORDS = {
    'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'dislike',
    'sad', 'angry', 'frustrated', 'disappointed', 'upset', 'annoyed',
    'poor', 'worst', 'fail', 'failure', 'problem', 'issue', 'wrong',
    'negative', 'pessimistic', 'depressed', 'miserable', 'unhappy'
}

# Stop words for keyword extraction
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
    'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
}

class DocumentAnalyzer:
    def __init__(self):
        self.documents = {}
        self._load_sample_documents()
    
    def _load_sample_documents(self):
        """Load 15+ sample documents with metadata"""
        sample_docs = [
            {
                'id': 'doc1',
                'title': 'Product Review - Smartphone',
                'content': 'This smartphone is absolutely amazing! The camera quality is excellent and the battery life is outstanding. I love the sleek design and the user interface is very intuitive. Highly recommended for anyone looking for a premium device.',
                'category': 'review',
                'author': 'John Smith',
                'date': '2024-01-15'
            },
            {
                'id': 'doc2',
                'title': 'Technical Documentation - API Guide',
                'content': 'The REST API provides endpoints for data retrieval and manipulation. Authentication is required using API keys. Rate limiting is implemented to ensure system stability. Error responses follow standard HTTP status codes.',
                'category': 'technical',
                'author': 'Tech Team',
                'date': '2024-01-10'
            },
            {
                'id': 'doc3',
                'title': 'Customer Complaint - Service Issue',
                'content': 'I am extremely disappointed with the service I received. The staff was rude and unhelpful. My order was delayed without any notification. This is unacceptable and I demand a full refund.',
                'category': 'complaint',
                'author': 'Jane Doe',
                'date': '2024-01-12'
            },
            {
                'id': 'doc4',
                'title': 'News Article - Climate Change',
                'content': 'Scientists report significant progress in renewable energy technology. Solar panel efficiency has improved by 20% in the last year. Wind energy production has reached record levels globally.',
                'category': 'news',
                'author': 'News Reporter',
                'date': '2024-01-08'
            },
            {
                'id': 'doc5',
                'title': 'Blog Post - Travel Experience',
                'content': 'My recent trip to Japan was incredible. The food was delicious, the people were friendly, and the scenery was breathtaking. I particularly enjoyed visiting the ancient temples and experiencing the traditional culture.',
                'category': 'blog',
                'author': 'Travel Blogger',
                'date': '2024-01-05'
            },
            {
                'id': 'doc6',
                'title': 'Academic Paper - Machine Learning',
                'content': 'This paper presents a novel approach to neural network optimization. The proposed algorithm demonstrates superior performance compared to existing methods. Experimental results show significant improvements in accuracy and computational efficiency.',
                'category': 'academic',
                'author': 'Dr. Research',
                'date': '2024-01-03'
            },
            {
                'id': 'doc7',
                'title': 'Product Manual - Coffee Machine',
                'content': 'Before using the coffee machine, ensure it is properly connected to power. Fill the water reservoir with clean water. Insert coffee pods into the designated compartment. Press the brew button to start the brewing process.',
                'category': 'manual',
                'author': 'Manufacturer',
                'date': '2024-01-01'
            },
            {
                'id': 'doc8',
                'title': 'Meeting Minutes - Project Planning',
                'content': 'The team discussed project milestones and deadlines. Budget allocation was reviewed and approved. Resource requirements were identified. Next meeting scheduled for next week to review progress.',
                'category': 'meeting',
                'author': 'Project Manager',
                'date': '2024-01-20'
            },
            {
                'id': 'doc9',
                'title': 'Email - Marketing Campaign',
                'content': 'Our latest marketing campaign has exceeded expectations. Click-through rates increased by 35% compared to previous campaigns. Customer engagement metrics show positive trends across all demographics.',
                'category': 'email',
                'author': 'Marketing Team',
                'date': '2024-01-18'
            },
            {
                'id': 'doc10',
                'title': 'Report - Sales Performance',
                'content': 'Q4 sales figures demonstrate strong performance across all product lines. Revenue increased by 15% year-over-year. Customer satisfaction scores remain consistently high. Market share has expanded in key regions.',
                'category': 'report',
                'author': 'Sales Director',
                'date': '2024-01-25'
            },
            {
                'id': 'doc11',
                'title': 'Story - Short Fiction',
                'content': 'The old lighthouse stood majestically on the rocky cliff. Waves crashed against the shore below as the keeper climbed the spiral staircase. The beacon light cut through the darkness, guiding ships safely to harbor.',
                'category': 'fiction',
                'author': 'Creative Writer',
                'date': '2024-01-22'
            },
            {
                'id': 'doc12',
                'title': 'Recipe - Chocolate Cake',
                'content': 'Preheat oven to 350 degrees. Mix flour, sugar, and cocoa powder in a large bowl. Add eggs, milk, and vanilla extract. Stir until smooth. Pour into greased pan and bake for 30 minutes.',
                'category': 'recipe',
                'author': 'Chef',
                'date': '2024-01-28'
            },
            {
                'id': 'doc13',
                'title': 'Policy Document - Remote Work',
                'content': 'Employees are permitted to work remotely up to three days per week. Proper equipment and internet connectivity are required. Regular check-ins with supervisors must be maintained. Performance standards remain unchanged.',
                'category': 'policy',
                'author': 'HR Department',
                'date': '2024-01-30'
            },
            {
                'id': 'doc14',
                'title': 'Tutorial - Web Development',
                'content': 'Creating responsive web designs requires understanding of CSS media queries. Start with mobile-first approach. Use flexible grid systems and scalable images. Test across multiple devices and screen sizes.',
                'category': 'tutorial',
                'author': 'Web Developer',
                'date': '2024-02-01'
            },
            {
                'id': 'doc15',
                'title': 'Press Release - Product Launch',
                'content': 'Company announces the launch of innovative new product line. Advanced features include AI-powered automation and enhanced security protocols. Product availability begins next month with nationwide distribution.',
                'category': 'press',
                'author': 'PR Team',
                'date': '2024-02-03'
            },
            {
                'id': 'doc16',
                'title': 'Survey Results - Customer Feedback',
                'content': 'Customer satisfaction survey reveals high approval ratings. 92% of respondents would recommend our services. Areas for improvement include response time and product variety. Overall sentiment remains positive.',
                'category': 'survey',
                'author': 'Research Team',
                'date': '2024-02-05'
            }
        ]
        
        for doc in sample_docs:
            self.documents[doc['id']] = doc
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using keyword-based approach"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        positive_count = sum(1 for word in words if word in POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in NEGATIVE_WORDS)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment = 'neutral'
            confidence = 0.5
        elif positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count - negative_count) / len(words))
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count - positive_count) / len(words))
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'positive_words': positive_count,
            'negative_words': negative_count
        }
    
    def extract_keywords(self, text: str, limit: int = 10) -> List[str]:
        """Extract top keywords from text"""
        # Clean and tokenize text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in STOP_WORDS and len(word) > 2]
        
        # Count word frequencies
        word_counts = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, count in word_counts.most_common(limit)]
    
    def calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics"""
        # Basic text statistics
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = re.findall(r'\b\w+\b', text)
        
        # Count syllables (simple approximation)
        def count_syllables(word):
            word = word.lower()
            vowels = 'aeiouy'
            syllable_count = 0
            prev_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_was_vowel:
                    syllable_count += 1
                prev_was_vowel = is_vowel
            
            # Handle silent e
            if word.endswith('e') and syllable_count > 1:
                syllable_count -= 1
            
            return max(1, syllable_count)
        
        total_syllables = sum(count_syllables(word) for word in words)
        
        if len(sentences) == 0 or len(words) == 0:
            return {
                'flesch_score': 0,
                'reading_level': 'Unknown',
                'avg_sentence_length': 0,
                'avg_syllables_per_word': 0
            }
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        
        # Flesch Reading Ease Score
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))
        
        # Determine reading level
        if flesch_score >= 90:
            reading_level = 'Very Easy'
        elif flesch_score >= 80:
            reading_level = 'Easy'
        elif flesch_score >= 70:
            reading_level = 'Fairly Easy'
        elif flesch_score >= 60:
            reading_level = 'Standard'
        elif flesch_score >= 50:
            reading_level = 'Fairly Difficult'
        elif flesch_score >= 30:
            reading_level = 'Difficult'
        else:
            reading_level = 'Very Difficult'
        
        return {
            'flesch_score': round(flesch_score, 1),
            'reading_level': reading_level,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 1)
        }
    
    def get_basic_stats(self, text: str) -> Dict[str, int]:
        """Get basic text statistics"""
        words = re.findall(r'\b\w+\b', text)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'character_count': len(text),
            'character_count_no_spaces': len(text.replace(' ', ''))
        }

# Initialize the analyzer
analyzer = DocumentAnalyzer()

# Create the MCP server
server = Server("document-analyzer")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="analyze_document",
            description="Perform full analysis of a document including sentiment, keywords, readability, and basic stats",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "ID of the document to analyze"
                    }
                },
                "required": ["document_id"]
            }
        ),
        types.Tool(
            name="get_sentiment",
            description="Analyze sentiment of any text (positive/negative/neutral)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze for sentiment"
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="extract_keywords",
            description="Extract top keywords from text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to extract keywords from"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of keywords to return",
                        "default": 10
                    }
                },
                "required": ["text"]
            }
        ),
        types.Tool(
            name="add_document",
            description="Add a new document to the collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "category": {"type": "string"},
                            "author": {"type": "string"},
                            "date": {"type": "string"}
                        },
                        "required": ["id", "title", "content"]
                    }
                },
                "required": ["document_data"]
            }
        ),
        types.Tool(
            name="search_documents",
            description="Search documents by content or metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find documents"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    
    if name == "analyze_document":
        document_id = arguments["document_id"]
        
        if document_id not in analyzer.documents:
            return [types.TextContent(
                type="text",
                text=f"Document with ID '{document_id}' not found."
            )]
        
        doc = analyzer.documents[document_id]
        content = doc['content']
        
        # Perform full analysis
        sentiment = analyzer.analyze_sentiment(content)
        keywords = analyzer.extract_keywords(content, 10)
        readability = analyzer.calculate_readability(content)
        stats = analyzer.get_basic_stats(content)
        
        result = {
            'document_info': {
                'id': doc['id'],
                'title': doc['title'],
                'category': doc.get('category', 'unknown'),
                'author': doc.get('author', 'unknown'),
                'date': doc.get('date', 'unknown')
            },
            'sentiment_analysis': sentiment,
            'keywords': keywords,
            'readability': readability,
            'basic_stats': stats
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_sentiment":
        text = arguments["text"]
        sentiment = analyzer.analyze_sentiment(text)
        
        return [types.TextContent(
            type="text",
            text=json.dumps(sentiment, indent=2)
        )]
    
    elif name == "extract_keywords":
        text = arguments["text"]
        limit = arguments.get("limit", 10)
        keywords = analyzer.extract_keywords(text, limit)
        
        return [types.TextContent(
            type="text",
            text=json.dumps({"keywords": keywords}, indent=2)
        )]
    
    elif name == "add_document":
        document_data = arguments["document_data"]
        doc_id = document_data["id"]
        
        if doc_id in analyzer.documents:
            return [types.TextContent(
                type="text",
                text=f"Document with ID '{doc_id}' already exists."
            )]
        
        # Add current date if not provided
        if "date" not in document_data:
            document_data["date"] = datetime.now().strftime("%Y-%m-%d")
        
        analyzer.documents[doc_id] = document_data
        
        return [types.TextContent(
            type="text",
            text=f"Document '{doc_id}' added successfully."
        )]
    
    elif name == "search_documents":
        query = arguments["query"].lower()
        matching_docs = []
        
        for doc_id, doc in analyzer.documents.items():
            # Search in title, content, category, and author
            searchable_text = f"{doc['title']} {doc['content']} {doc.get('category', '')} {doc.get('author', '')}".lower()
            
            if query in searchable_text:
                matching_docs.append({
                    'id': doc['id'],
                    'title': doc['title'],
                    'category': doc.get('category', 'unknown'),
                    'author': doc.get('author', 'unknown'),
                    'date': doc.get('date', 'unknown'),
                    'content_preview': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content']
                })
        
        result = {
            'query': arguments["query"],
            'total_matches': len(matching_docs),
            'documents': matching_docs
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [types.TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="document-analyzer",
                server_version="1.0.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability(listChanged=False)
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())