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

- [ ] Define heading dictionaries for Turkish and English section names.
- [ ] Detect contact information.
- [ ] Detect professional summary or profile.
- [ ] Detect skills.
- [ ] Detect work experience.
- [ ] Detect education.
- [ ] Detect projects.
- [ ] Detect certifications.
- [ ] Assign each section one status: `present`, `weak`, or `missing`.
- [ ] Mark sections weak when they are short, generic, or lack useful job-relevant detail.
- [ ] Generate Turkish section messages for each section result.

## M5 - Embeddings and Scoring

- [ ] Add `sentence-transformers` dependency.
- [ ] Use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- [ ] Load the embedding model lazily or at application startup.
- [ ] Generate an embedding for cleaned CV text.
- [ ] Generate an embedding for cleaned job-description text.
- [ ] Calculate cosine similarity.
- [ ] Clamp semantic similarity to `0..1`.
- [ ] Calculate keyword match ratio.
- [ ] Calculate section score using `present = 1.0`, `weak = 0.5`, `missing = 0.0`.
- [ ] Combine score components with weights: 50% semantic similarity, 30% keyword match, 20% section completeness.
- [ ] Round the final score to the nearest integer.
- [ ] Clamp `overall_score` to `0..100`.

## M6 - Feedback Generation

- [ ] Implement deterministic Turkish feedback templates.
- [ ] Generate feedback based on score range: low, moderate, good, strong.
- [ ] Mention missing keywords conditionally.
- [ ] Avoid instructing users to add skills they do not actually have.
- [ ] Prioritize the most important gaps.
- [ ] Keep suggestions practical, specific, clear, and encouraging.

## M7 - Analyze API

- [ ] Implement `POST /api/v1/analyze`.
- [ ] Accept `multipart/form-data`.
- [ ] Use form field `cv_file`.
- [ ] Use form field `job_description`.
- [ ] Connect validation, extraction, cleaning, section detection, keyword matching, embeddings, scoring, and feedback services.
- [ ] Return `overall_score`.
- [ ] Return `semantic_similarity`.
- [ ] Return `matched_keywords`.
- [ ] Return `missing_keywords`.
- [ ] Return `section_analysis`.
- [ ] Return `suggestions`.
- [ ] Return `extracted_cv_text_preview`.
- [ ] Ensure response schema matches `docs/API_SPEC.md`.
- [ ] Return `400` with `MISSING_FILE` for missing file.
- [ ] Return `400` with `EMPTY_JOB_DESCRIPTION` for empty job description.
- [ ] Return `415` with `UNSUPPORTED_FILE_TYPE` for unsupported uploads.
- [ ] Return `413` with `FILE_TOO_LARGE` for oversized uploads.
- [ ] Return `422` with `TEXT_EXTRACTION_FAILED` for unreadable files.
- [ ] Return `500` with `ANALYSIS_FAILED` for unexpected analysis failures.

## M8 - Frontend

- [ ] Create `frontend/index.html`.
- [ ] Create `frontend/styles.css`.
- [ ] Create `frontend/app.js`.
- [ ] Build the first screen as the usable analysis workflow.
- [ ] Add CV file input.
- [ ] Add job-description textarea.
- [ ] Add Analyze button.
- [ ] Add basic client-side required-field validation.
- [ ] Show initial empty state.
- [ ] Show loading state while analysis runs.
- [ ] Show success state with results.
- [ ] Show error state from API validation failures.
- [ ] Send request to `/api/v1/analyze`.
- [ ] Display overall score prominently.
- [ ] Display semantic similarity.
- [ ] Display matched keywords.
- [ ] Display missing keywords.
- [ ] Display section analysis.
- [ ] Display Turkish suggestions.
- [ ] Display extracted CV text preview as secondary or collapsed content.
- [ ] Keep frontend plain HTML, CSS, and JavaScript.

## M9 - Docker

- [ ] Add `Dockerfile`.
- [ ] Add `docker-compose.yml`.
- [ ] Use one FastAPI container for the MVP.
- [ ] Install required system dependencies for PDF libraries if needed.
- [ ] Expose port `8000`.
- [ ] Configure `uvicorn` startup command.
- [ ] Optionally serve static frontend files from FastAPI.
- [ ] Document Docker usage in `README.md`.

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
