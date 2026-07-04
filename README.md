# SmartCV Analyzer

AI-powered CV analysis system for comparing a resume with a pasted job description and generating practical improvement feedback.

## Project Description

SmartCV Analyzer is a portfolio-focused software project built around a simple workflow:

1. Upload a CV or resume file.
2. Paste a job description.
3. Click Analyze.
4. View compatibility results and improvement suggestions.

The system extracts text from PDF or DOCX CV files, detects important CV sections, extracts job description keywords, compares the CV with the job description, calculates semantic similarity with a multilingual embedding model, and returns Turkish user-facing feedback.

The application interface, API, code comments, endpoint names, and documentation are written in English. Analysis results and suggestions shown to users are generated in Turkish.

## Features

### MVP Features

- Upload PDF and DOCX CV files
- Paste job description manually
- Extract text from uploaded CV files
- Detect important CV sections:
  - Contact information
  - Professional summary or profile
  - Skills
  - Work experience
  - Education
  - Projects
  - Certifications
- Extract keywords from the job description
- Match job description keywords against CV content
- Detect missing keywords
- Calculate semantic similarity using `sentence-transformers`
- Generate an overall compatibility score from 0 to 100
- Return Turkish feedback and improvement suggestions
- Provide a simple HTML/CSS/JavaScript frontend
- Provide FastAPI automatic API documentation
- Run with Docker and docker-compose
- Include a Postman testing plan

### Out of Scope for MVP

- User authentication
- User accounts
- Database storage
- Job posting URL scraping
- Paid AI APIs
- Multi-document analysis
- General report analysis
- Advanced applicant tracking system features

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, FastAPI |
| NLP | sentence-transformers, scikit-learn, spaCy or KeyBERT optional |
| Embeddings | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| PDF extraction | PyMuPDF or pdfplumber |
| DOCX extraction | python-docx |
| Frontend | HTML, CSS, JavaScript |
| API testing | Postman |
| Containerization | Docker, docker-compose |

## Recommended Model

Use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` for the MVP.

Reasons:

- Supports Turkish and English
- Works locally without paid APIs
- Small enough for a portfolio project
- Good balance between quality and performance
- Easy to use with the `sentence-transformers` library

## Screenshots

Screenshots will be added after the MVP frontend is implemented.

Suggested screenshot list:

- Upload and job description form
- Loading or analysis state
- Analysis result page
- Keyword match section
- Section analysis section

## Installation

> Code implementation is not part of the current documentation phase. These instructions define the expected setup after implementation.

### Local Setup

```bash
git clone https://github.com/your-username/smartcv-analyzer.git
cd smartcv-analyzer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend should run at:

```text
http://localhost:8000
```

FastAPI documentation should be available at:

```text
http://localhost:8000/docs
```

## Docker Usage

Build and start the MVP with one FastAPI container:

```bash
docker compose up --build
```

The app will be available at:

```text
http://localhost:8000
```

Useful endpoints:

- Frontend: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Analyze API: `http://localhost:8000/api/v1/analyze`

Stop the container:

```bash
docker compose down
```

The Compose setup runs a single `smartcv-api` service. The static frontend is served by FastAPI, and no database, Redis, nginx, or separate frontend container is required for the MVP.

The first CV analysis inside Docker may take longer because the `sentence-transformers` embedding model can be downloaded on first use. Model files are not committed to the repository.

## API Usage

Main endpoint:

```http
POST /api/v1/analyze
```

Request type:

```text
multipart/form-data
```

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `cv_file` | File | Yes | PDF or DOCX CV file |
| `job_description` | String | Yes | Manually pasted job description |

Example response fields:

```json
{
  "overall_score": 78,
  "semantic_similarity": 0.82,
  "matched_keywords": ["Python", "FastAPI", "Docker"],
  "missing_keywords": ["Kubernetes", "CI/CD"],
  "section_analysis": [],
  "suggestions": [],
  "extracted_cv_text_preview": "..."
}
```

See [API_SPEC.md](./API_SPEC.md) for the full API contract.

## Postman Testing

The project should include a Postman collection after implementation.

Minimum test scenarios:

- Valid PDF upload
- Valid DOCX upload
- Missing file
- Empty job description
- Unsupported file type
- Large file
- Corrupted or unreadable file

See [POSTMAN_TEST_PLAN.md](./POSTMAN_TEST_PLAN.md) for the full test plan.

## Example Output

```json
{
  "overall_score": 78,
  "semantic_similarity": 0.82,
  "matched_keywords": ["Python", "FastAPI", "Docker", "REST API"],
  "missing_keywords": ["CI/CD", "Kubernetes"],
  "section_analysis": [
    {
      "section": "Projects",
      "status": "weak",
      "message": "Projeler bölümü mevcut ancak teknik detaylar ve ölçülebilir çıktılar daha görünür olmalı."
    }
  ],
  "suggestions": [
    "CV'nize CI/CD ve Kubernetes deneyiminizi destekleyen örnekler eklemeniz önerilir.",
    "Projeler bölümünde kullandığınız teknolojileri ve elde ettiğiniz sonuçları daha net belirtin."
  ],
  "extracted_cv_text_preview": "Software Developer with experience in Python..."
}
```

## Documentation

- [PRD.md](./PRD.md)
- [TECHNICAL_ARCHITECTURE.md](./TECHNICAL_ARCHITECTURE.md)
- [API_SPEC.md](./API_SPEC.md)
- [SCORING_LOGIC.md](./SCORING_LOGIC.md)
- [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)
- [POSTMAN_TEST_PLAN.md](./POSTMAN_TEST_PLAN.md)

## Future Improvements

- User accounts and saved analysis history
- Database support
- Multiple CV versions per user
- Job description URL import
- More advanced Turkish NLP
- ATS-style formatting checks
- Export analysis as PDF
- Admin dashboard for usage analytics
- Support for additional file types
- Model comparison and configurable scoring weights

## Portfolio Value

This project demonstrates practical software engineering skills across backend development, NLP, file processing, API design, frontend integration, Docker, and technical documentation. It is intentionally scoped as a realistic junior to mid-level developer portfolio project while still showing applied AI and product thinking.
