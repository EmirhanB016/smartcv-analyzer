# AGENTS.md

Guidance for coding agents working on SmartCV Analyzer.

## Source Documents

Read the documents in `docs/` before implementing behavior. They are the product and technical source of truth:

- `docs/PRD.md`: product scope, MVP goals, non-goals, success criteria
- `docs/TECHNICAL_ARCHITECTURE.md`: recommended folder structure and pipeline design
- `docs/API_SPEC.md`: API routes, request fields, response schema, validation errors
- `docs/SCORING_LOGIC.md`: keyword, section, similarity, and scoring rules
- `docs/DEVELOPMENT_PLAN.md`: milestone order and implementation checklist
- `docs/POSTMAN_TEST_PLAN.md`: manual/API verification scenarios

If implementation and docs disagree, prefer the docs for intended MVP behavior and call out the mismatch.

## Product Scope

SmartCV Analyzer is an MVP web app for comparing one uploaded CV/resume against one manually pasted job description. The app should extract CV text, analyze it against the job description, calculate a 0-100 compatibility score, and return Turkish user-facing feedback.

Keep the MVP intentionally simple:

- No authentication or user accounts
- No database or saved analysis history
- No payment features
- No paid AI APIs
- No job-posting scraping
- No browser extension
- No multi-file comparison
- No general document-analysis features

Use open-source local libraries and deterministic logic for the MVP.

## Architecture Expectations

Backend should be FastAPI. Recommended structure:

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

Frontend should stay plain HTML, CSS, and JavaScript unless requirements change:

```text
frontend/
  index.html
  styles.css
  app.js
```

Serving the static frontend from FastAPI is acceptable for the MVP. Avoid adding a frontend framework unless there is a clear new requirement.

## API Contract

Implement:

- `GET /health`
- `POST /api/v1/analyze`

`POST /api/v1/analyze` accepts `multipart/form-data`:

- `cv_file`: required PDF or DOCX file
- `job_description`: required string, recommended minimum 50 characters

Successful responses must include:

- `overall_score`: integer from 0 to 100
- `semantic_similarity`: float from 0 to 1
- `matched_keywords`: string array
- `missing_keywords`: string array
- `section_analysis`: array of section status objects
- `suggestions`: Turkish string array
- `extracted_cv_text_preview`: string

Expected validation failures:

- Missing file: `400`, code `MISSING_FILE`
- Empty job description: `400`, code `EMPTY_JOB_DESCRIPTION`
- Unsupported file type: `415`, code `UNSUPPORTED_FILE_TYPE`
- File too large: `413`, code `FILE_TOO_LARGE`
- Text extraction failure: `422`, code `TEXT_EXTRACTION_FAILED`
- Unexpected analysis failure: `500`, code `ANALYSIS_FAILED`

FastAPI docs should be available at `/docs` and `/redoc`. Endpoint descriptions, code, and general docs should be English. User-facing analysis messages should be Turkish.

## File Handling

Support only:

- `.pdf`
- `.docx`

Recommended MVP file size limit is 5 MB.

Process uploads in memory or temporary storage only. Do not persist uploaded CV files in the MVP. Do not commit personal CV samples or sensitive data.

Recommended libraries:

- PDF extraction: `PyMuPDF`
- DOCX extraction: `python-docx`

Reject unreadable or empty extracted text with `TEXT_EXTRACTION_FAILED`.

## NLP Pipeline

Follow this pipeline:

1. Clean CV and job-description text.
2. Normalize whitespace and casing for matching.
3. Preserve Turkish characters.
4. Extract job-description keywords.
5. Match keywords against CV text.
6. Detect missing keywords.
7. Detect CV sections.
8. Calculate semantic similarity.
9. Calculate score.
10. Generate deterministic Turkish feedback.

Keyword extraction should start simple:

- Remove common Turkish and English stop words.
- Extract unigrams, bigrams, and selected trigrams.
- Prefer technical terms, tools, frameworks, responsibilities, and methodologies.
- Deduplicate case-insensitively.
- Limit output to the top 20-30 keywords.
- Use a small synonym/variant map for common software terms when useful.

## Section Detection

Detect these CV sections:

- Contact information
- Professional summary or profile
- Skills
- Work experience
- Education
- Projects
- Certifications

Each section status must be one of:

- `present`
- `weak`
- `missing`

Use heading-based detection for Turkish and English headings. Mark a section `weak` when it exists but is too short, generic, light on relevant keywords, or lacks useful details such as technologies, responsibilities, outcomes, or impact.

## Embeddings and Scoring

Use the multilingual sentence-transformers model recommended in the docs:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Load the model lazily or at application startup. Calculate cosine similarity and clamp it to `0..1`.

Overall score formula:

```text
overall_score =
  (semantic_similarity * 50)
  + (keyword_match_ratio * 30)
  + (section_score * 20)
```

Where:

- `keyword_match_ratio = matched_keywords_count / total_extracted_keywords_count`
- section values are `present = 1.0`, `weak = 0.5`, `missing = 0.0`
- `section_score` is the average section value

Round the final score to the nearest integer and clamp it to `0..100`.

## Feedback Rules

Generate feedback with deterministic Turkish templates for the MVP. Feedback should:

- Be practical and specific.
- Avoid telling users to claim skills they do not have.
- Mention missing keywords conditionally.
- Prioritize the most important gaps.
- Stay clear and encouraging.

## Frontend Requirements

The first screen should be the usable analysis workflow, not a marketing page.

Include:

- CV file input
- Job-description text area
- Analyze button
- Client-side required-field validation
- Loading state
- Success state
- Error state

Display:

- Overall score
- Semantic similarity
- Matched keywords
- Missing keywords
- Section analysis
- Turkish suggestions
- Extracted CV text preview, preferably secondary or collapsed

## Testing Expectations

Add tests in proportion to the change. Prioritize:

- Text cleaning
- File extension and size validation
- Keyword extraction and matching
- Section detection
- Score calculation
- Analyze endpoint success for PDF and DOCX
- Missing file
- Empty job description
- Unsupported file type
- Text extraction failure

Manual/Postman scenarios are documented in `docs/POSTMAN_TEST_PLAN.md`. The local base URL is expected to be:

```text
http://localhost:8000
```

## Development Order

Prefer the milestone order in `docs/DEVELOPMENT_PLAN.md`:

1. FastAPI project structure and health endpoint
2. File validation and text extraction
3. Text cleaning, keyword extraction, and section detection
4. Embeddings and scoring
5. Turkish feedback generation
6. Complete `/api/v1/analyze`
7. Simple frontend
8. Docker setup
9. Tests and Postman collection
10. README/screenshots/GitHub polish

Implement one milestone at a time when possible.

## Repository Hygiene

- Keep code and API docs in English.
- Keep user-facing analysis feedback in Turkish.
- Keep the MVP modular; separate API, schemas, services, and utilities.
- Avoid overengineering with queues, Redis, PostgreSQL, auth, or background jobs unless requirements change.
- Keep secrets, uploaded files, model caches, virtual environments, and personal CV data out of git.
- Before changing existing files, check the current worktree and preserve unrelated user changes.
