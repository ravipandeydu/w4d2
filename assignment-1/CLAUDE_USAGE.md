# Using Document Analyzer in Claude Desktop

This guide shows you exactly how to use the Document Analyzer MCP Server within Claude Desktop with natural language commands and practical examples.

## 🚀 Quick Start in Claude

Once your MCP server is configured (see <mcfile name="CLAUDE_SETUP.md" path="c:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1\CLAUDE_SETUP.md"></mcfile>), you can start analyzing documents immediately using natural language.

## 💬 Natural Language Commands

### 1. Document Analysis Commands

#### Complete Document Analysis
```
"Analyze the document tech_article_1"
"Give me a full analysis of business_report_2"
"What can you tell me about science_paper_1?"
```

**What you'll get**:
- Sentiment analysis (positive/negative/neutral)
- Key topics and keywords
- Readability score and grade level
- Text statistics (word count, sentences, etc.)

#### Sentiment Analysis Only
```
"What's the sentiment of news_article_1?"
"Is tech_article_2 positive or negative?"
"Analyze the emotional tone of business_report_3"
```

#### Keyword Extraction
```
"Extract keywords from science_paper_2"
"What are the main topics in tech_article_1?"
"Give me 15 keywords from business_report_1"
```

#### Readability Analysis
```
"How readable is science_paper_1?"
"What's the reading level of news_article_2?"
"Is tech_article_3 easy to understand?"
```

### 2. Document Management Commands

#### Adding New Documents
```
"Add a new document with ID 'my_essay' titled 'Climate Change Essay' with this content: [paste your text]"

"Store this document as 'meeting_notes_jan' in the business category: [paste meeting notes]"
```

#### Searching Documents
```
"Find documents about artificial intelligence"
"Search for documents containing 'climate change'"
"What documents mention 'blockchain'?"
```

#### Listing Available Documents
```
"What documents are available?"
"Show me all the sample documents"
"List documents in the technology category"
```

## 📋 Available Sample Documents

You can analyze any of these pre-loaded documents:

### Technology Documents
- `tech_article_1` - "The Future of Artificial Intelligence"
- `tech_article_2` - "Blockchain Revolution"
- `tech_article_3` - "Quantum Computing Breakthrough"
- `tech_article_4` - "5G Network Implementation"

### Business Documents
- `business_report_1` - "Q4 Financial Performance"
- `business_report_2` - "Market Analysis Report"
- `business_report_3` - "Strategic Planning Document"
- `business_report_4` - "Customer Satisfaction Survey"

### Science Documents
- `science_paper_1` - "Climate Change Impact Study"
- `science_paper_2` - "Genetic Engineering Research"
- `science_paper_3` - "Space Exploration Mission"
- `science_paper_4` - "Renewable Energy Solutions"

### News Documents
- `news_article_1` - "Global Economic Outlook"
- `news_article_2` - "Healthcare Innovation"
- `news_article_3` - "Educational Reform Initiative"
- `news_article_4` - "Environmental Conservation Efforts"

## 🎯 Practical Usage Examples

### Example 1: Content Research

**You**: "Find documents about climate change and analyze their sentiment"

**Claude will**:
1. Search for documents containing "climate change"
2. Find `science_paper_1` and `news_article_4`
3. Analyze the sentiment of both documents
4. Compare their emotional tones

### Example 2: Writing Analysis

**You**: "I want to check if my writing is too complex. Add this document and analyze its readability: [paste your text]"

**Claude will**:
1. Add your document to the collection
2. Calculate readability scores
3. Tell you the grade level and difficulty
4. Suggest if it's appropriate for your target audience

### Example 3: Content Comparison

**You**: "Compare the sentiment and keywords between tech_article_1 and tech_article_2"

**Claude will**:
1. Analyze both documents
2. Extract keywords from each
3. Compare sentiment scores
4. Highlight similarities and differences

### Example 4: Topic Discovery

**You**: "What are the main themes across all business documents?"

**Claude will**:
1. Extract keywords from all business documents
2. Identify common themes
3. Summarize the main topics
4. Show frequency of key terms

## 📊 Understanding the Results

### Sentiment Analysis Results
```
Sentiment: positive (75% confidence)
Positive indicators: 8 positive words found
Negative indicators: 2 negative words found
Overall tone: Optimistic and forward-looking
```

### Keyword Extraction Results
```
Top Keywords:
1. artificial (appears 12 times)
2. intelligence (appears 10 times)
3. technology (appears 8 times)
4. future (appears 6 times)
5. innovation (appears 5 times)
```

### Readability Analysis Results
```
Flesch Reading Ease: 65.2 (Standard difficulty)
Flesch-Kincaid Grade Level: 8.5 (8th-9th grade)
Recommendation: Suitable for general adult audience
```

### Text Statistics Results
```
Word Count: 245 words
Sentence Count: 12 sentences
Paragraph Count: 4 paragraphs
Average Sentence Length: 20.4 words
```

## 🔄 Workflow Examples

### Academic Research Workflow

1. **Discovery**: "Find documents about renewable energy"
2. **Analysis**: "Analyze the sentiment of science_paper_4"
3. **Keywords**: "Extract key terms from science_paper_4"
4. **Comparison**: "How does this compare to other science documents?"

### Content Creation Workflow

1. **Add Content**: "Store my blog post as 'ai_blog_post' with this content: [paste]"
2. **Check Readability**: "What's the reading level of ai_blog_post?"
3. **Sentiment Check**: "Is the tone of ai_blog_post appropriate?"
4. **Keyword Review**: "What are the main topics in ai_blog_post?"

### Business Analysis Workflow

1. **Search**: "Find all business-related documents"
2. **Sentiment Trends**: "What's the overall sentiment across business documents?"
3. **Key Themes**: "What topics appear most frequently in business documents?"
4. **Readability**: "Are our business documents too complex for stakeholders?"

## 💡 Pro Tips for Claude Usage

### 1. Be Specific with Document IDs
```
✅ Good: "Analyze tech_article_1"
❌ Avoid: "Analyze the tech article"
```

### 2. Combine Multiple Requests
```
✅ Good: "Analyze sentiment and extract keywords from business_report_1"
✅ Good: "Compare readability between science_paper_1 and news_article_1"
```

### 3. Use Natural Language
```
✅ Good: "Is this document positive or negative?"
✅ Good: "What grade level is this written for?"
✅ Good: "What are the main topics discussed?"
```

### 4. Ask for Explanations
```
✅ Good: "Why is this document rated as difficult to read?"
✅ Good: "What makes this sentiment positive?"
✅ Good: "Explain the keyword extraction results"
```

### 5. Request Comparisons
```
✅ Good: "Which document is more positive: tech_article_1 or tech_article_2?"
✅ Good: "Compare the complexity of science papers vs news articles"
```

## 🚨 Common Issues and Solutions

### Issue: "Document not found"
**Solution**: Use exact document IDs from the available list above

### Issue: "Server not responding"
**Solution**: Check your MCP configuration in Claude Desktop settings

### Issue: "Analysis seems incomplete"
**Solution**: Ask for specific aspects: "What's the sentiment?" or "Extract keywords"

### Issue: "Can't add new documents"
**Solution**: Ensure you provide all required fields: ID, title, and content

## 🎨 Creative Usage Ideas

### 1. Content Optimization
"Help me make this document more readable for a general audience"

### 2. Tone Adjustment
"This document seems too negative. What words are causing this?"

### 3. SEO Analysis
"What keywords should I focus on based on this document analysis?"

### 4. Audience Targeting
"Is this content appropriate for high school students?"

### 5. Content Strategy
"What topics are missing from our business document collection?"

## 📈 Advanced Analysis Requests

### Multi-Document Analysis
```
"Compare sentiment across all technology documents"
"What keywords appear in both business and science documents?"
"Which category has the most positive sentiment overall?"
```

### Trend Analysis
```
"Show me sentiment trends across different document categories"
"What's the average readability score for each category?"
"Which documents are most similar in terms of keywords?"
```

### Custom Analysis
```
"Create a summary report of all document statistics"
"Rank documents by readability from easiest to hardest"
"Find the most and least positive documents"
```

## 🎯 Getting Started Checklist

- [ ] MCP server configured in Claude Desktop
- [ ] Server running without errors
- [ ] Test with: "What documents are available?"
- [ ] Try analyzing: "Analyze tech_article_1"
- [ ] Test search: "Find documents about technology"
- [ ] Add your own document for analysis

Once you've completed this checklist, you're ready to use the full power of document analysis within Claude Desktop!

## 🔗 Related Resources

- <mcfile name="CLAUDE_SETUP.md" path="c:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1\CLAUDE_SETUP.md"></mcfile> - Setup and troubleshooting
- <mcfile name="USAGE_GUIDE.md" path="c:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1\USAGE_GUIDE.md"></mcfile> - Technical documentation
- <mcfile name="README.md" path="c:\Users\Admin\Documents\misogiai\week-4\w4d2\assignment-1\README.md"></mcfile> - Project overview

Start with simple commands like "Analyze tech_article_1" and gradually explore more complex analysis requests as you become familiar with the system!