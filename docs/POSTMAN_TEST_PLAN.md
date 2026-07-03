# Postman Test Plan

## Overview

This document defines the Postman testing plan for the SmartCV Analyzer MVP. The purpose is to verify the FastAPI endpoints, request validation, file upload behavior, and response structure.

## Postman Collection

Recommended collection name:

```text
SmartCV Analyzer
```

Recommended environment:

| Variable | Value |
| --- | --- |
| `base_url` | `http://localhost:8000` |

## Endpoints to Test

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `{{base_url}}/health` | Verify API is running |
| `POST` | `{{base_url}}/api/v1/analyze` | Analyze uploaded CV against job description |

## Test Case Summary

| ID | Scenario | Expected Status |
| --- | --- | --- |
| TC-001 | Health check | 200 |
| TC-002 | Valid PDF upload | 200 |
| TC-003 | Valid DOCX upload | 200 |
| TC-004 | Missing file | 400 |
| TC-005 | Empty job description | 400 |
| TC-006 | Unsupported file type | 415 |
| TC-007 | Large file | 413 |
| TC-008 | Corrupted or unreadable file | 422 |

## TC-001: Health Check

### Request

```http
GET {{base_url}}/health
```

### Expected Response

```json
{
  "status": "ok"
}
```

## TC-002: Valid PDF Upload Scenario

### Request

```http
POST {{base_url}}/api/v1/analyze
Content-Type: multipart/form-data
```

### Form Data

| Key | Type | Value |
| --- | --- | --- |
| `cv_file` | File | `sample_cv.pdf` |
| `job_description` | Text | Realistic software developer job description |

### Expected Response

Status:

```text
200 OK
```

Expected fields:

```json
{
  "overall_score": 78,
  "semantic_similarity": 0.82,
  "matched_keywords": ["Python", "FastAPI"],
  "missing_keywords": ["Kubernetes"],
  "section_analysis": [],
  "suggestions": [],
  "extracted_cv_text_preview": "..."
}
```

Validation checks:

- `overall_score` is between 0 and 100.
- `semantic_similarity` is between 0 and 1.
- `matched_keywords` is an array.
- `missing_keywords` is an array.
- `section_analysis` is an array.
- `suggestions` is an array.
- Suggestions are written in Turkish.
- `extracted_cv_text_preview` is not empty.

## TC-003: Valid DOCX Upload Scenario

### Request

```http
POST {{base_url}}/api/v1/analyze
Content-Type: multipart/form-data
```

### Form Data

| Key | Type | Value |
| --- | --- | --- |
| `cv_file` | File | `sample_cv.docx` |
| `job_description` | Text | Realistic software developer job description |

### Expected Response

Status:

```text
200 OK
```

Expected behavior:

- DOCX text is extracted successfully.
- Response schema matches the API spec.
- Turkish feedback is returned.

## TC-004: Missing File Scenario

### Request

Send only `job_description`, without `cv_file`.

### Expected Response

Status:

```text
400 Bad Request
```

Body:

```json
{
  "detail": {
    "code": "MISSING_FILE",
    "message": "CV file is required."
  }
}
```

## TC-005: Empty Job Description Scenario

### Request

Send `cv_file` with an empty `job_description`.

### Expected Response

Status:

```text
400 Bad Request
```

Body:

```json
{
  "detail": {
    "code": "EMPTY_JOB_DESCRIPTION",
    "message": "Job description must not be empty."
  }
}
```

## TC-006: Unsupported File Type Scenario

### Request

Upload a `.txt`, `.png`, or `.zip` file as `cv_file`.

### Expected Response

Status:

```text
415 Unsupported Media Type
```

Body:

```json
{
  "detail": {
    "code": "UNSUPPORTED_FILE_TYPE",
    "message": "Only PDF and DOCX files are supported."
  }
}
```

## TC-007: Large File Scenario

### Request

Upload a PDF or DOCX file larger than the configured MVP limit, recommended 5 MB.

### Expected Response

Status:

```text
413 Payload Too Large
```

Body:

```json
{
  "detail": {
    "code": "FILE_TOO_LARGE",
    "message": "The uploaded file exceeds the 5 MB size limit."
  }
}
```

## TC-008: Corrupted or Unreadable File Scenario

### Request

Upload a corrupted PDF or DOCX file.

### Expected Response

Status:

```text
422 Unprocessable Entity
```

Body:

```json
{
  "detail": {
    "code": "TEXT_EXTRACTION_FAILED",
    "message": "Could not extract readable text from the uploaded CV."
  }
}
```

## Suggested Postman Test Scripts

### Success Response Script

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response contains required fields", function () {
  const json = pm.response.json();
  pm.expect(json).to.have.property("overall_score");
  pm.expect(json).to.have.property("semantic_similarity");
  pm.expect(json).to.have.property("matched_keywords");
  pm.expect(json).to.have.property("missing_keywords");
  pm.expect(json).to.have.property("section_analysis");
  pm.expect(json).to.have.property("suggestions");
  pm.expect(json).to.have.property("extracted_cv_text_preview");
});

pm.test("Score is between 0 and 100", function () {
  const json = pm.response.json();
  pm.expect(json.overall_score).to.be.at.least(0);
  pm.expect(json.overall_score).to.be.at.most(100);
});
```

### Error Response Script

```javascript
pm.test("Response contains error detail", function () {
  const json = pm.response.json();
  pm.expect(json).to.have.property("detail");
  pm.expect(json.detail).to.have.property("code");
  pm.expect(json.detail).to.have.property("message");
});
```

## Manual Verification Checklist

- Health endpoint returns 200.
- Analyze endpoint accepts PDF.
- Analyze endpoint accepts DOCX.
- API rejects unsupported files.
- API rejects empty job descriptions.
- API response fields match `API_SPEC.md`.
- User-facing suggestions are Turkish.
- Score values are numeric and within expected ranges.
- No uploaded file is permanently stored in the MVP.
