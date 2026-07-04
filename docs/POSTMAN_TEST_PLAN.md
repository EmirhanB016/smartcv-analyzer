# Postman Test Plan

## Overview

This document defines manual Postman verification for the SmartCV Analyzer MVP. The goal is to confirm the FastAPI app, file upload behavior, validation errors, and response schema using the exported Postman collection.

## Files

Import these files into Postman:

```text
postman/SmartCV_Analyzer.postman_collection.json
postman/SmartCV_Analyzer.postman_environment.json
```

Collection name:

```text
SmartCV Analyzer
```

Environment name:

```text
SmartCV Analyzer Local
```

Environment variable:

| Variable | Value |
| --- | --- |
| `base_url` | `http://localhost:8000` |

## Import Steps

1. Open Postman.
2. Select **Import**.
3. Import `postman/SmartCV_Analyzer.postman_collection.json`.
4. Import `postman/SmartCV_Analyzer.postman_environment.json`.
5. Select the `SmartCV Analyzer Local` environment from the environment selector.
6. Confirm `base_url` is set to `http://localhost:8000`.

## Start The App

### Local Python

```bash
python -m uvicorn app.main:app --reload
```

### Docker

```bash
docker compose up
```

The app should be available at:

```text
http://localhost:8000
```

Useful URLs:

- Frontend: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Analyze endpoint: `http://localhost:8000/api/v1/analyze`

The first analysis may take longer because the `sentence-transformers` model can be downloaded or loaded on first use.

## Test Files To Select Manually

The Postman collection does not hardcode local file paths. For file upload requests, select local files manually in Postman.

Use personal-safe or synthetic files only:

| Request | File to select |
| --- | --- |
| Analyze CV - Valid PDF | A readable `.pdf` CV or small synthetic PDF |
| Analyze CV - Valid DOCX | A readable `.docx` CV or small synthetic DOCX |
| Analyze CV - Empty Job Description | Any readable `.pdf` or `.docx` CV |
| Analyze CV - Unsupported File Type | A `.txt`, `.png`, `.zip`, or other unsupported file |
| Analyze CV - Large File | A `.pdf` or `.docx` file larger than 5 MB |
| Analyze CV - Corrupted or Unreadable File | A corrupted PDF or invalid DOCX |

Do not commit real personal CVs, uploaded files, or model caches.

Scanned or image-only PDFs may return `TEXT_EXTRACTION_FAILED` because OCR is not included in the MVP.

## Requests

| ID | Request | Method | Expected Status |
| --- | --- | --- | --- |
| TC-001 | Health Check | `GET` | `200` |
| TC-002 | Analyze CV - Valid PDF | `POST` | `200` |
| TC-003 | Analyze CV - Valid DOCX | `POST` | `200` |
| TC-004 | Analyze CV - Missing File | `POST` | `400` |
| TC-005 | Analyze CV - Empty Job Description | `POST` | `400` |
| TC-006 | Analyze CV - Unsupported File Type | `POST` | `415` |
| TC-007 | Analyze CV - Large File | `POST` | `413` |
| TC-008 | Analyze CV - Corrupted or Unreadable File | `POST` | `422` |

## Success Response Shape

Successful analyze responses should include:

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

Postman tests assert:

- Status code is `200`.
- `overall_score` exists and is between `0` and `100`.
- `semantic_similarity` exists and is between `0` and `1`.
- `matched_keywords` is an array.
- `missing_keywords` is an array.
- `section_analysis` is an array.
- `suggestions` is an array.
- `extracted_cv_text_preview` exists.

Manual checks:

- Suggestions and section messages should be Turkish.
- The score should be plausible for the selected CV and job description.
- The extracted text preview should not contain unrelated local file data.

## Error Response Shape

Validation errors should follow this shape:

```json
{
  "detail": {
    "code": "MISSING_FILE",
    "message": "CV file is required."
  }
}
```

Postman tests assert:

- The expected status code is returned.
- `detail.code` exists.
- `detail.message` exists.
- The expected error code is returned for each negative request.

## Expected Error Codes

| Scenario | Status | Code |
| --- | ---: | --- |
| Missing file | `400` | `MISSING_FILE` |
| Empty job description | `400` | `EMPTY_JOB_DESCRIPTION` |
| Unsupported file type | `415` | `UNSUPPORTED_FILE_TYPE` |
| File larger than 5 MB | `413` | `FILE_TOO_LARGE` |
| Corrupted or unreadable file | `422` | `TEXT_EXTRACTION_FAILED` |

The implemented API accepts an optional upload field at the FastAPI boundary and maps a missing file to the documented custom `MISSING_FILE` response.

## Manual Verification Checklist

- Import the collection and environment successfully.
- Select the `SmartCV Analyzer Local` environment.
- Confirm every request URL uses `{{base_url}}`.
- Run `Health Check` and confirm `{"status": "ok"}`.
- Run valid PDF and DOCX requests with selected local files.
- Confirm success responses include all required fields.
- Confirm `overall_score` is within `0..100`.
- Confirm `semantic_similarity` is within `0..1`.
- Confirm suggestions and section messages are Turkish.
- Run each negative request and confirm the expected `detail.code`.
- Confirm no local absolute file paths are stored in the collection.
- Confirm uploaded files are not written permanently by the application.
