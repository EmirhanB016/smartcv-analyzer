# API Specification

## Overview

The MVP exposes a small FastAPI API for analyzing one uploaded CV against one manually pasted job description.

Base URL for local development:

```text
http://localhost:8000
```

API version prefix:

```text
/api/v1
```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/analyze` | Analyze CV against job description |

## Health Check

### Request

```http
GET /health
```

### Success Response

```json
{
  "status": "ok"
}
```

## Analyze CV

### Request

```http
POST /api/v1/analyze
Content-Type: multipart/form-data
```

### Form Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `cv_file` | File | Yes | Uploaded CV file. Must be PDF or DOCX. |
| `job_description` | String | Yes | Job description pasted manually by the user. |

### Validation Rules

| Rule | Requirement |
| --- | --- |
| File required | `cv_file` must be provided |
| Supported file types | `.pdf`, `.docx` |
| Max file size | Recommended MVP limit: 5 MB |
| Job description required | `job_description` must not be empty |
| Minimum job description length | Recommended: 50 characters |
| Extracted CV text | Must contain readable text |

## Example Request

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -F "cv_file=@sample_cv.pdf" \
  -F "job_description=We are looking for a Python developer with FastAPI, Docker, SQL, REST API, and CI/CD experience."
```

### JavaScript Fetch

```javascript
const formData = new FormData();
formData.append("cv_file", fileInput.files[0]);
formData.append("job_description", jobDescriptionTextarea.value);

const response = await fetch("/api/v1/analyze", {
  method: "POST",
  body: formData
});

const result = await response.json();
```

## Success Response

### Status Code

```text
200 OK
```

### Response Body

```json
{
  "overall_score": 78,
  "semantic_similarity": 0.82,
  "matched_keywords": [
    "Python",
    "FastAPI",
    "Docker",
    "REST API"
  ],
  "missing_keywords": [
    "CI/CD",
    "Kubernetes"
  ],
  "section_analysis": [
    {
      "section": "Contact information",
      "status": "present",
      "message": "İletişim bilgileri CV'nizde mevcut görünüyor."
    },
    {
      "section": "Projects",
      "status": "weak",
      "message": "Projeler bölümü mevcut ancak teknik detaylar daha görünür olmalı."
    },
    {
      "section": "Certifications",
      "status": "missing",
      "message": "Sertifikalar bölümü bulunamadı. Varsa ilgili sertifikalarınızı ekleyebilirsiniz."
    }
  ],
  "suggestions": [
    "CV'niz iş ilanıyla genel olarak iyi düzeyde uyumlu görünüyor.",
    "CI/CD ve Kubernetes deneyiminiz varsa bu anahtar kelimeleri daha görünür şekilde eklemeniz önerilir.",
    "Projeler bölümünde kullandığınız teknolojileri, sorumluluklarınızı ve ölçülebilir sonuçları daha net belirtin."
  ],
  "extracted_cv_text_preview": "Software Developer with experience in Python, FastAPI, Docker and REST API development..."
}
```

## Response Field Definitions

| Field | Type | Description |
| --- | --- | --- |
| `overall_score` | Integer | Final compatibility score from 0 to 100 |
| `semantic_similarity` | Float | Cosine similarity between CV and job description, from 0 to 1 |
| `matched_keywords` | Array of strings | Job description keywords found in the CV |
| `missing_keywords` | Array of strings | Important job description keywords not found in the CV |
| `section_analysis` | Array of objects | Status and Turkish feedback for important CV sections |
| `suggestions` | Array of strings | Turkish improvement suggestions |
| `extracted_cv_text_preview` | String | Short preview of extracted CV text for debugging and transparency |

## Section Analysis Object

```json
{
  "section": "Skills",
  "status": "present",
  "message": "Yetenekler bölümü CV'nizde mevcut görünüyor."
}
```

| Field | Type | Allowed Values |
| --- | --- | --- |
| `section` | String | Human-readable section name |
| `status` | String | `present`, `weak`, `missing` |
| `message` | String | Turkish explanation |

## Error Responses

### Missing File

```text
400 Bad Request
```

```json
{
  "detail": {
    "code": "MISSING_FILE",
    "message": "CV file is required."
  }
}
```

### Empty Job Description

```text
400 Bad Request
```

```json
{
  "detail": {
    "code": "EMPTY_JOB_DESCRIPTION",
    "message": "Job description must not be empty."
  }
}
```

### Unsupported File Type

```text
415 Unsupported Media Type
```

```json
{
  "detail": {
    "code": "UNSUPPORTED_FILE_TYPE",
    "message": "Only PDF and DOCX files are supported."
  }
}
```

### File Too Large

```text
413 Payload Too Large
```

```json
{
  "detail": {
    "code": "FILE_TOO_LARGE",
    "message": "The uploaded file exceeds the 5 MB size limit."
  }
}
```

### Text Extraction Failed

```text
422 Unprocessable Entity
```

```json
{
  "detail": {
    "code": "TEXT_EXTRACTION_FAILED",
    "message": "Could not extract readable text from the uploaded CV."
  }
}
```

### Internal Error

```text
500 Internal Server Error
```

```json
{
  "detail": {
    "code": "ANALYSIS_FAILED",
    "message": "An unexpected error occurred during analysis."
  }
}
```

## FastAPI Documentation

FastAPI should automatically expose:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

Endpoint descriptions should be written in English. User-facing analysis messages inside successful responses should be Turkish.
