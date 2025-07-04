#!/usr/bin/env python3
"""
Test script for Document Analyzer MCP Server
Demonstrates all available tools and their functionality.
"""

import asyncio
import json
from server import analyzer

async def test_document_analyzer():
    """Test all functionality of the document analyzer"""
    
    print("=" * 60)
    print("DOCUMENT ANALYZER MCP SERVER - TEST SUITE")
    print("=" * 60)
    
    # Test 1: List available documents
    print("\n1. AVAILABLE DOCUMENTS:")
    print("-" * 30)
    for doc_id, doc in analyzer.documents.items():
        print(f"ID: {doc_id} | Title: {doc['title']} | Category: {doc.get('category', 'N/A')}")
    
    # Test 2: Analyze a specific document
    print("\n2. FULL DOCUMENT ANALYSIS (doc1 - Smartphone Review):")
    print("-" * 50)
    doc = analyzer.documents['doc1']
    content = doc['content']
    
    sentiment = analyzer.analyze_sentiment(content)
    keywords = analyzer.extract_keywords(content, 10)
    readability = analyzer.calculate_readability(content)
    stats = analyzer.get_basic_stats(content)
    
    print(f"Document: {doc['title']}")
    print(f"Content: {content}")
    print(f"\nSentiment Analysis: {json.dumps(sentiment, indent=2)}")
    print(f"\nTop Keywords: {keywords}")
    print(f"\nReadability Metrics: {json.dumps(readability, indent=2)}")
    print(f"\nBasic Statistics: {json.dumps(stats, indent=2)}")
    
    # Test 3: Sentiment analysis on different types of text
    print("\n3. SENTIMENT ANALYSIS TESTS:")
    print("-" * 35)
    
    test_texts = [
        "I absolutely love this product! It's amazing and wonderful!",
        "This is terrible and awful. I hate it completely.",
        "The weather is cloudy today. It might rain later.",
        "The technical documentation provides comprehensive API endpoints."
    ]
    
    for i, text in enumerate(test_texts, 1):
        sentiment = analyzer.analyze_sentiment(text)
        print(f"Text {i}: {text}")
        print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']})")
        print()
    
    # Test 4: Keyword extraction
    print("\n4. KEYWORD EXTRACTION TESTS:")
    print("-" * 35)
    
    keyword_texts = [
        "Machine learning algorithms are revolutionizing artificial intelligence applications in modern technology.",
        "The restaurant serves delicious Italian cuisine with fresh ingredients and excellent service.",
        "Climate change affects global weather patterns and environmental sustainability worldwide."
    ]
    
    for i, text in enumerate(keyword_texts, 1):
        keywords = analyzer.extract_keywords(text, 5)
        print(f"Text {i}: {text}")
        print(f"Top 5 Keywords: {keywords}")
        print()
    
    # Test 5: Readability analysis
    print("\n5. READABILITY ANALYSIS TESTS:")
    print("-" * 35)
    
    readability_texts = [
        "The cat sat on the mat. It was a sunny day.",  # Simple text
        "The implementation of sophisticated algorithms requires comprehensive understanding of computational complexity theory.",  # Complex text
        "Machine learning encompasses various methodologies including supervised, unsupervised, and reinforcement learning paradigms."  # Technical text
    ]
    
    for i, text in enumerate(readability_texts, 1):
        readability = analyzer.calculate_readability(text)
        print(f"Text {i}: {text}")
        print(f"Flesch Score: {readability['flesch_score']} ({readability['reading_level']})")
        print(f"Avg Sentence Length: {readability['avg_sentence_length']} words")
        print(f"Avg Syllables per Word: {readability['avg_syllables_per_word']}")
        print()
    
    # Test 6: Add new document
    print("\n6. ADD NEW DOCUMENT TEST:")
    print("-" * 30)
    
    new_doc = {
        'id': 'test_doc',
        'title': 'Test Document',
        'content': 'This is a test document created to verify the add document functionality. It contains positive words like excellent and amazing.',
        'category': 'test',
        'author': 'Test User',
        'date': '2024-02-10'
    }
    
    # Check if document exists before adding
    if 'test_doc' not in analyzer.documents:
        analyzer.documents['test_doc'] = new_doc
        print(f"Added new document: {new_doc['title']}")
        
        # Analyze the new document
        new_content = new_doc['content']
        new_sentiment = analyzer.analyze_sentiment(new_content)
        print(f"New document sentiment: {new_sentiment['sentiment']} (confidence: {new_sentiment['confidence']})")
    else:
        print("Test document already exists")
    
    # Test 7: Search documents
    print("\n7. DOCUMENT SEARCH TESTS:")
    print("-" * 30)
    
    search_queries = ['machine learning', 'excellent', 'customer', 'technical']
    
    for query in search_queries:
        matching_docs = []
        query_lower = query.lower()
        
        for doc_id, doc in analyzer.documents.items():
            searchable_text = f"{doc['title']} {doc['content']} {doc.get('category', '')} {doc.get('author', '')}".lower()
            if query_lower in searchable_text:
                matching_docs.append({
                    'id': doc['id'],
                    'title': doc['title'],
                    'category': doc.get('category', 'unknown')
                })
        
        print(f"Query: '{query}' - Found {len(matching_docs)} matches")
        for match in matching_docs[:3]:  # Show first 3 matches
            print(f"  - {match['id']}: {match['title']} ({match['category']})")
        print()
    
    # Test 8: Statistics summary
    print("\n8. DOCUMENT COLLECTION STATISTICS:")
    print("-" * 40)
    
    total_docs = len(analyzer.documents)
    categories = {}
    total_words = 0
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for doc in analyzer.documents.values():
        # Count categories
        category = doc.get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1
        
        # Count words
        stats = analyzer.get_basic_stats(doc['content'])
        total_words += stats['word_count']
        
        # Count sentiments
        sentiment = analyzer.analyze_sentiment(doc['content'])
        sentiment_counts[sentiment['sentiment']] += 1
    
    print(f"Total Documents: {total_docs}")
    print(f"Total Words: {total_words:,}")
    print(f"Average Words per Document: {total_words // total_docs}")
    print(f"\nCategories:")
    for category, count in sorted(categories.items()):
        print(f"  - {category}: {count}")
    print(f"\nSentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / total_docs) * 100
        print(f"  - {sentiment.title()}: {count} ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_document_analyzer())