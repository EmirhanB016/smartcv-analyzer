# SmartCV Analyzer Tasks

Implementation task board derived from the documents in `docs/`.

## MVP Guardrails

- [ ] Keep the MVP focused on one CV/resume file matched against one manually pasted job description.
- [ ] Do not add authentication, user accounts, database persistence, payments, scraping, browser extensions, or paid AI APIs.
- [ ] Keep UI, docs, API names, and code in English.
- [ ] Keep user-facing analysis feedback in Turkish.
- [ ] Process uploaded files in memory or temporary storage only.
- [ ] Do not commit personal CV samples, secrets, uploaded files, virtual environments, or model caches.

## M1 - Project Setup

- [x] Create the recommended FastAPI structure under `app/`.
- [x] Add `app/main.py`.
- [x] Add `app/api/routes.py`.
- [x] Add `app/core/config.py`.
- [x] Add schema modules for analysis and errors.
- [x] Add service modules for file extraction, section detection, keywords, embeddings, scoring, and feedback.
- [x] Add utility modules for text cleaning and validators.
- [x] Add dependency management for the backend.
- [x] Configure FastAPI app title and version.
- [x] Add `/health` endpoint returning `{"status": "ok"}`.
- [x] Add `/api/v1` router.
- [x] Expose FastAPI docs at `/docs` and `/redoc`.

## M2 - File Validation and Extraction

- [x] Implement required `cv_file` validation.
- [x] Implement required `job_description` validation.
- [x] Enforce supported file extensions: `.pdf`, `.docx`.
- [x] Enforce recommended 5 MB file size limit.
- [x] Validate content type when practical.
- [x] Implement PDF text extraction with `PyMuPDF`.
- [x] Implement DOCX text extraction with `python-docx`.
- [x] Extract DOCX paragraphs and table text where practical.
- [x] Return `TEXT_EXTRACTION_FAILED` when readable CV text cannot be extracted.
- [x] Ensure uploaded CV files are not permanently stored.

## M3 - Text Cleaning and NLP Basics

- [x] Implement whitespace normalization.
- [x] Remove excessive blank lines.
- [x] Trim leading and trailing text.
- [x] Preserve Turkish characters in display text.
- [x] Create lowercase normalized copies for matching.
- [x] Define Turkish and English stop-word lists.
- [x] Implement rule-based keyword extraction from job descriptions.
- [x] Extract unigrams, bigrams, and selected trigrams.
- [x] Prefer technical terms, tools, frameworks, responsibilities, and methodologies.
- [x] Deduplicate keywords case-insensitively.
- [x] Limit extracted keywords to the top 20-30 terms.
- [x] Add a small synonym/variant map for common software terms.
- [x] Implement case-insensitive keyword matching against CV text.
- [x] Support phrase matching for terms such as `REST API` and `machine learning`.
- [x] Calculate `matched_keywords`.
- [x] Calculate `missing_keywords`.

## M4 - Section Detection

- [x] Define heading dictionaries for Turkish and English section names.
- [x] Detect contact information.
- [x] Detect professional summary or profile.
- [x] Detect skills.
- [x] Detect work experience.
- [x] Detect education.
- [x] Detect projects.
- [x] Detect certifications.
- [x] Assign each section one status: `present`, `weak`, or `missing`.
- [x] Mark sections weak when they are short, generic, or lack useful job-relevant detail.
- [x] Generate Turkish section messages for each section result.

## M5 - Embeddings and Scoring

- [x] Add `sentence-transformers` dependency.
- [x] Use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- [x] Load the embedding model lazily or at application startup.
- [x] Generate an embedding for cleaned CV text.
- [x] Generate an embedding for cleaned job-description text.
- [x] Calculate cosine similarity.
- [x] Clamp semantic similarity to `0..1`.
- [x] Calculate keyword match ratio.
- [x] Calculate section score using `present = 1.0`, `weak = 0.5`, `missing = 0.0`.
- [x] Combine score components with weights: 50% semantic similarity, 30% keyword match, 20% section completeness.
- [x] Round the final score to the nearest integer.
- [x] Clamp `overall_score` to `0..100`.

## M6 - Feedback Generation

- [x] Implement deterministic Turkish feedback templates.
- [x] Generate feedback based on score range: low, moderate, good, strong.
- [x] Mention missing keywords conditionally.
- [x] Avoid instructing users to add skills they do not actually have.
- [x] Prioritize the most important gaps.
- [x] Keep suggestions practical, specific, clear, and encouraging.

## M7 - Analyze API

- [x] Implement `POST /api/v1/analyze`.
- [x] Accept `multipart/form-data`.
- [x] Use form field `cv_file`.
- [x] Use form field `job_description`.
- [x] Connect validation, extraction, cleaning, section detection, keyword matching, embeddings, scoring, and feedback services.
- [x] Return `overall_score`.
- [x] Return `semantic_similarity`.
- [x] Return `matched_keywords`.
- [x] Return `missing_keywords`.
- [x] Return `section_analysis`.
- [x] Return `suggestions`.
- [x] Return `extracted_cv_text_preview`.
- [x] Ensure response schema matches `docs/API_SPEC.md`.
- [x] Return `400` with `MISSING_FILE` for missing file.
- [x] Return `400` with `EMPTY_JOB_DESCRIPTION` for empty job description.
- [x] Return `415` with `UNSUPPORTED_FILE_TYPE` for unsupported uploads.
- [x] Return `413` with `FILE_TOO_LARGE` for oversized uploads.
- [x] Return `422` with `TEXT_EXTRACTION_FAILED` for unreadable files.
- [x] Return `500` with `ANALYSIS_FAILED` for unexpected analysis failures.

## M8 - Frontend

- [x] Create `frontend/index.html`.
- [x] Create `frontend/styles.css`.
- [x] Create `frontend/app.js`.
- [x] Build the first screen as the usable analysis workflow.
- [x] Add CV file input.
- [x] Add job-description textarea.
- [x] Add Analyze button.
- [x] Add basic client-side required-field validation.
- [x] Show initial empty state.
- [x] Show loading state while analysis runs.
- [x] Show success state with results.
- [x] Show error state from API validation failures.
- [x] Send request to `/api/v1/analyze`.
- [x] Display overall score prominently.
- [x] Display semantic similarity.
- [x] Display matched keywords.
- [x] Display missing keywords.
- [x] Display section analysis.
- [x] Display Turkish suggestions.
- [x] Display extracted CV text preview as secondary or collapsed content.
- [x] Keep frontend plain HTML, CSS, and JavaScript.

## M9 - Docker

- [x] Add `Dockerfile`.
- [x] Add `docker-compose.yml`.
- [x] Use one FastAPI container for the MVP.
- [x] Install required system dependencies for PDF libraries if needed.
- [x] Expose port `8000`.
- [x] Configure `uvicorn` startup command.
- [x] Optionally serve static frontend files from FastAPI.
- [x] Document Docker usage in `README.md`.

## M10 - Automated Tests

- [ ] Add test dependencies: `pytest` and `httpx`.
- [ ] Test text cleaning.
- [ ] Test file extension validation.
- [ ] Test file size validation.
- [ ] Test keyword extraction.
- [ ] Test keyword matching.
- [ ] Test section detection.
- [ ] Test score calculation.
- [ ] Test health endpoint.
- [ ] Test analyze endpoint with valid PDF.
- [ ] Test analyze endpoint with valid DOCX.
- [ ] Test missing file error.
- [ ] Test empty job description error.
- [ ] Test unsupported file type error.
- [ ] Test text extraction failure.

## M11 - Postman and Manual Verification

- [ ] Create Postman collection named `SmartCV Analyzer`.
- [ ] Add Postman environment variable `base_url = http://localhost:8000`.
- [ ] Add health check request.
- [ ] Add valid PDF upload request.
- [ ] Add valid DOCX upload request.
- [ ] Add missing file negative request.
- [ ] Add empty job description negative request.
- [ ] Add unsupported file type negative request.
- [ ] Add large file negative request.
- [ ] Add corrupted or unreadable file negative request.
- [ ] Add success response assertions for required fields.
- [ ] Add score range assertion for `overall_score`.
- [ ] Add semantic similarity range assertion.
- [ ] Add error response assertions for `detail.code` and `detail.message`.
- [ ] Manually verify that suggestions are Turkish.
- [ ] Manually verify no uploaded file is permanently stored.

## M12 - GitHub Polish

- [ ] Update `README.md` with clear project description.
- [ ] Add installation instructions.
- [ ] Add local development instructions.
- [ ] Add Docker instructions.
- [ ] Add API usage examples.
- [ ] Add screenshots.
- [ ] Add realistic example response.
- [ ] Confirm docs are complete and consistent.
- [ ] Confirm `.gitignore` excludes virtual environments, cache files, uploaded files, and model caches.
- [ ] Confirm `LICENSE` is present.
- [ ] Confirm no paid API keys or secrets are required.
- [ ] Confirm no sample personal CV data is committed.

## Acceptance Checklist

- [ ] A user can upload a PDF CV and receive an analysis.
- [ ] A user can upload a DOCX CV and receive an analysis.
- [ ] A user can paste a Turkish, English, or mixed job description.
- [ ] API returns all required fields from `docs/API_SPEC.md`.
- [ ] Overall score is reproducible from documented scoring logic.
- [ ] Matched and missing keywords are returned.
- [ ] Missing or weak CV sections are identified.
- [ ] Semantic similarity is included as a `0..1` value.
- [ ] Suggestions are understandable and useful in Turkish.
- [ ] Typical analysis completes within 5-15 seconds on a development machine after model load.
- [ ] Project runs locally with Docker.
- [ ] Repository remains simple, modular, and portfolio-friendly.
