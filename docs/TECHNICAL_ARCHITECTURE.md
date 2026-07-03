# Technical Architecture

## System Architecture

SmartCV Analyzer is a lightweight web application with a FastAPI backend and a simple frontend. The backend handles file validation, text extraction, NLP analysis, scoring, and response generation. The frontend handles file upload, job description input, and result display.

```text
Browser
  |
  | multipart/form-data
  v
FastAPI Backend
  |
  |-- File validation
  |-- PDF/DOCX text extraction
  |-- CV section detection
  |-- Keyword extraction
  |-- Keyword matching
  |-- Embedding similarity
  |-- Score calculation
  |-- Turkish feedback generation
  v
JSON Response
  |
  v
Frontend Result View
```

## Backend Architecture

Recommended backend structure:

```text
app/
  main.py
  api/
    routes.py
  core/
    config.py
  schemas/
    analysis.py
    errors.py
  services/
    file_extraction_service.py
    section_detection_service.py
    keyword_service.py
    embedding_service.py
    scoring_service.py
    feedback_service.py
  utils/
    text_cleaning.py
    validators.py
```

### Backend Responsibilities

- Accept multipart form uploads
- Validate file extension and size
- Extract text from PDF or DOCX
- Normalize extracted text
- Extract job description keywords
- Detect CV sections
- Calculate semantic similarity
- Calculate overall score
- Generate Turkish feedback
- Return a structured API response

## Frontend Architecture

The MVP frontend should use plain HTML, CSS, and JavaScript.

Recommended frontend structure:

```text
frontend/
  index.html
  styles.css
  app.js
```

### Frontend Responsibilities

- Render upload form
- Render job description text area
- Validate basic required fields before submit
- Show loading state during analysis
- Send request to `/api/v1/analyze`
- Display:
  - Overall score
  - Semantic similarity
  - Matched keywords
  - Missing keywords
  - Section analysis
  - Suggestions
  - CV text preview

The frontend should stay simple and avoid a framework unless future requirements justify it.

## NLP Pipeline

Recommended pipeline:

1. Clean CV text and job description text.
2. Normalize whitespace and casing for matching.
3. Extract keywords from the job description.
4. Match extracted keywords against CV text.
5. Detect missing keywords.
6. Generate embeddings for the CV and job description.
7. Calculate cosine similarity.
8. Feed keyword, section, and similarity results into the scoring service.

## File Processing Pipeline

```text
Uploaded file
  |
  |-- Validate extension: .pdf or .docx
  |-- Validate content type when possible
  |-- Validate file size
  v
Text extraction
  |
  |-- PDF: PyMuPDF or pdfplumber
  |-- DOCX: python-docx
  v
Text cleaning
  |
  |-- Normalize whitespace
  |-- Remove excessive line breaks
  |-- Trim empty content
  v
Analysis pipeline
```

### PDF Extraction

Recommended library: `PyMuPDF`

Reasons:

- Fast
- Good text extraction support
- Simple API

Alternative: `pdfplumber`, especially if layout-aware extraction becomes important.

### DOCX Extraction

Recommended library: `python-docx`

Reasons:

- Stable and commonly used
- Good enough for extracting paragraphs and table text in MVP

## CV Section Detection

The MVP can use rule-based detection. The service should look for common Turkish and English section headings.

Example heading groups:

| Section | Example Headings |
| --- | --- |
| Contact | Contact, Contact Information, İletişim |
| Summary | Summary, Profile, Professional Summary, Özet, Profil |
| Skills | Skills, Technical Skills, Yetenekler, Teknik Yetenekler |
| Experience | Experience, Work Experience, İş Deneyimi, Deneyim |
| Education | Education, Eğitim |
| Projects | Projects, Projeler |
| Certifications | Certifications, Certificates, Sertifikalar |

Each section can be classified as:

- `present`
- `weak`
- `missing`

## Keyword Pipeline

The MVP should avoid overengineering. A practical keyword extraction approach:

1. Clean the job description.
2. Tokenize into words and short phrases.
3. Remove stop words in Turkish and English.
4. Keep likely technical keywords and noun phrases.
5. Deduplicate keywords case-insensitively.
6. Limit to the top 20 to 30 keywords.

Recommended implementation options:

- Simple rule-based extraction for MVP
- `scikit-learn` `TfidfVectorizer` for phrase ranking
- Optional future enhancement: KeyBERT

## Embedding and Similarity Pipeline

Recommended model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Embedding steps:

1. Load model once at application startup or lazily on first request.
2. Generate one embedding for cleaned CV text.
3. Generate one embedding for cleaned job description text.
4. Calculate cosine similarity.
5. Normalize similarity into a 0 to 1 value.

## Scoring Pipeline

The overall score should combine:

| Component | Weight |
| --- | ---: |
| Semantic similarity | 50% |
| Keyword match ratio | 30% |
| Section completeness | 20% |

Example formula:

```text
overall_score =
  (semantic_similarity * 50)
  + (keyword_match_ratio * 30)
  + (section_score * 20)
```

The final score should be rounded to the nearest integer and clamped between 0 and 100.

## Docker Architecture

MVP Docker setup:

```text
docker-compose.yml
  |
  |-- api service
      |-- FastAPI
      |-- sentence-transformers model
      |-- file extraction libraries
      |-- optional static frontend serving
```

Recommended approach for MVP:

- Use one FastAPI container.
- Serve frontend static files from FastAPI if desired.
- Avoid a separate frontend build system.
- Do not include database containers.

## Data Flow Explanation

1. Browser sends CV file and job description.
2. FastAPI validates request.
3. File extraction service extracts CV text.
4. Text cleaning utility normalizes CV and job description.
5. Section detection service checks CV structure.
6. Keyword service extracts job keywords and matches them against CV text.
7. Embedding service calculates semantic similarity.
8. Scoring service calculates overall score.
9. Feedback service generates Turkish suggestions.
10. API returns JSON response.
11. Frontend renders results.

## Recommended Libraries

| Purpose | Library |
| --- | --- |
| API framework | fastapi |
| ASGI server | uvicorn |
| File upload support | python-multipart |
| PDF extraction | PyMuPDF |
| DOCX extraction | python-docx |
| Embeddings | sentence-transformers |
| Similarity utilities | scikit-learn |
| Numerical operations | numpy |
| Validation | pydantic |
| Testing | pytest, httpx |
| Optional keyword extraction | KeyBERT |

## Future Architecture Improvements

- Add PostgreSQL for saved analysis history.
- Add background processing for large files.
- Add Redis or task queue only if analysis becomes slow.
- Add user authentication.
- Add export-to-PDF analysis reports.
- Add model configuration through environment variables.
