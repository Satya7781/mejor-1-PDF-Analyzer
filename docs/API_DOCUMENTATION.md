# 🔌 API Documentation

## Web API Endpoints

The Flask web application provides RESTful API endpoints for programmatic access to PDF processing capabilities.

### Base URL
```
http://localhost:5000/api
```

---

## 📤 File Upload & Processing

### `POST /api/upload`

Upload and process a PDF file with optional AI analysis.

#### Request
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): PDF file to process
  - `processing_type` (optional): `"basic"` or `"advanced"` (default: `"basic"`)
  - `persona` (optional): User persona for AI analysis
  - `task` (optional): Task description for AI ranking

#### Response
```json
{
  "success": true,
  "result": {
    "title": "Document Title",
    "outline": [
      {
        "level": "H1",
        "text": "Section Title",
        "page": 1
      }
    ],
    "raw_text": [
      {
        "page": 1,
        "text": "Page content..."
      }
    ],
    "tables": [
      {
        "page": 1,
        "data": [["A", "B"], ["1", "2"]]
      }
    ],
    "ranked_sections": [
      {
        "section": {
          "text": "Section Title",
          "page": 1,
          "level": "H1"
        },
        "score": 0.85
      }
    ]
  },
  "result_file": "result_20241005_123456_document.json"
}
```

#### Example
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@document.pdf" \
  -F "processing_type=advanced" \
  -F "persona=Business Analyst" \
  -F "task=Extract financial metrics"
```

---

## 🏆 Challenge 1B Processing

### `GET /api/challenge1b`

Process Challenge 1B collections with pre-loaded data (fast).

#### Response
```json
{
  "success": true,
  "collections_processed": 3,
  "results": {
    "Collection 1": {
      "metadata": {
        "persona": "Travel Planner",
        "job_to_be_done": "Plan a 4-day trip...",
        "input_documents": ["doc1.pdf", "doc2.pdf"]
      },
      "extracted_sections": [...],
      "subsection_analysis": [...]
    }
  },
  "note": "Using pre-processed results for instant demo"
}
```

### `GET /api/challenge1b/reprocess`

Reprocess Challenge 1B collections (full processing - takes time).

---

## 📥 File Download

### `GET /api/download/<filename>`

Download processed result files.

#### Parameters
- `filename`: Name of the result file to download

#### Response
- **Content-Type**: `application/json`
- **File**: JSON result file

---

## 🔍 Health Check

### `GET /api/health`

Check API health status.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "version": "1.0.0"
}
```

---

## 🐍 Python API Usage

### Basic Processing
```python
import requests

# Upload and process PDF
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/upload',
        files={'file': f},
        data={'processing_type': 'basic'}
    )

result = response.json()
print(f"Title: {result['result']['title']}")
```

### Advanced AI Analysis
```python
import requests

# AI-powered analysis
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/upload',
        files={'file': f},
        data={
            'processing_type': 'advanced',
            'persona': 'Researcher',
            'task': 'Find methodology and results sections'
        }
    )

result = response.json()
for section in result['result']['ranked_sections']:
    print(f"Section: {section['section']['text']}")
    print(f"Relevance: {section['score']:.2%}")
```

### Challenge 1B Processing
```python
import requests

# Process Challenge 1B
response = requests.get('http://localhost:5000/api/challenge1b')
data = response.json()

print(f"Collections processed: {data['collections_processed']}")
for collection, result in data['results'].items():
    print(f"{collection}: {len(result['extracted_sections'])} sections")
```

---

## 🔧 Direct Library Usage

### Core PDF Processing
```python
from parser import PDFOutlineParser
from pipeline import DocumentPipeline

# Using the parser directly
parser = PDFOutlineParser()
outline = parser.extract_outline("document.pdf")

# Using the full pipeline
pipeline = DocumentPipeline()
result = pipeline.process("document.pdf")
```

### AI Components
```python
from app.embedder import embed, embed_texts
from app.ranker import rank_sections

# Generate embeddings
text_vector = embed("Sample text")
vectors = embed_texts(["Text 1", "Text 2"])

# Rank sections
task_vector = embed("Find financial information")
sections = [{"text": "Budget", "page": 1}, {"text": "Revenue", "page": 2}]
ranked = rank_sections(sections, task_vector, top_k=5)
```

---

## ⚠️ Error Handling

### Common Error Responses
```json
{
  "error": "Error message",
  "success": false
}
```

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: File not found
- `413`: File too large (>50MB)
- `500`: Internal server error

### Error Examples
```json
// File too large
{
  "error": "File size exceeds 50MB limit",
  "success": false
}

// Invalid file type
{
  "error": "Only PDF files are allowed",
  "success": false
}

// Processing error
{
  "error": "Failed to extract text from PDF",
  "success": false
}
```

---

## 🚀 Performance Notes

- **Basic processing**: 5-10 seconds for typical documents
- **Advanced AI analysis**: 30-60 seconds depending on document size
- **Challenge 1B**: 2 seconds (pre-processed) or 2+ minutes (full reprocessing)
- **File size limit**: 50MB per upload
- **Concurrent requests**: Supported with multiprocessing

---

## 🔐 Security Considerations

- Files are temporarily stored and automatically cleaned up
- No persistent storage of uploaded documents
- Input validation on all parameters
- File type restrictions (PDF only)
- Size limits to prevent abuse

For production deployment, consider adding:
- Authentication/authorization
- Rate limiting
- HTTPS encryption
- Input sanitization
- Audit logging
