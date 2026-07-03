# Development Plan

## Implementation Strategy

Build the project in small milestones. Start with the backend API and a deterministic analysis pipeline, then add the frontend, Docker setup, tests, and GitHub polish. Avoid adding authentication, database storage, or paid AI services in the MVP.

## Milestones

| Milestone | Goal | Output |
| --- | --- | --- |
| M1 | Project setup | FastAPI app structure, dependencies, health endpoint |
| M2 | File extraction | PDF and DOCX text extraction services |
| M3 | NLP basics | Text cleaning, keyword extraction, section detection |
| M4 | Embeddings and scoring | Semantic similarity and overall score |
| M5 | Feedback generation | Turkish suggestions and section messages |
| M6 | API completion | `/api/v1/analyze` endpoint with validation |
| M7 | Frontend | Simple upload and result interface |
| M8 | Docker | Dockerfile and docker-compose |
| M9 | Testing | Unit, integration, and Postman test coverage |
| M10 | GitHub polish | README, screenshots, examples, cleanup |

## Recommended Task Order

1. Create FastAPI project structure.
2. Add dependency management.
3. Implement health endpoint.
4. Implement file validation.
5. Implement PDF text extraction.
6. Implement DOCX text extraction.
7. Implement text cleaning utilities.
8. Implement CV section detection.
9. Implement keyword extraction.
10. Implement keyword matching.
11. Add sentence-transformers embedding service.
12. Implement scoring service.
13. Implement Turkish feedback service.
14. Implement `/api/v1/analyze`.
15. Add error handling and validation.
16. Build simple frontend.
17. Add Docker setup.
18. Add tests.
19. Add Postman collection.
20. Add screenshots and final README polish.

## Backend Tasks

### Project Setup

- Create `app/main.py`.
- Configure FastAPI app title and version.
- Add CORS middleware if frontend is served separately.
- Add `/health` endpoint.
- Add `/api/v1` router.

### Request Validation

- Validate required file field.
- Validate required job description field.
- Validate supported extensions: `.pdf`, `.docx`.
- Validate maximum file size, recommended 5 MB.
- Return clear error codes.

### API Endpoint

- Implement `POST /api/v1/analyze`.
- Accept `multipart/form-data`.
- Return response matching `API_SPEC.md`.
- Use Pydantic response schemas.

## NLP Tasks

### Text Cleaning

- Normalize whitespace.
- Remove repeated blank lines.
- Trim leading and trailing text.
- Preserve Turkish characters.
- Create lowercase normalized copies for matching.

### Section Detection

- Define section heading dictionaries in Turkish and English.
- Detect section headings in extracted CV text.
- Estimate section length.
- Mark sections as `present`, `weak`, or `missing`.
- Generate Turkish section messages.

### Keyword Extraction

- Start with rule-based extraction plus stop word filtering.
- Support common software terms.
- Extract one-word and multi-word phrases.
- Deduplicate keywords.
- Limit result to top 20 to 30 keywords.

### Embeddings

- Install `sentence-transformers`.
- Use `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- Load model lazily or during startup.
- Generate embeddings for CV and job description.
- Calculate cosine similarity.

### Scoring

- Calculate keyword match ratio.
- Calculate section score.
- Calculate semantic similarity.
- Combine weighted components:
  - 50% semantic similarity
  - 30% keyword match
  - 20% section completeness
- Clamp score between 0 and 100.

## Frontend Tasks

### Form

- Add CV file input.
- Add job description text area.
- Add Analyze button.
- Add basic client-side validation.

### Result View

- Show overall score prominently.
- Show semantic similarity.
- Show matched keywords.
- Show missing keywords.
- Show section analysis.
- Show Turkish suggestions.
- Show extracted CV text preview in a collapsed or secondary area.

### UX States

- Initial empty state.
- Loading state.
- Success state.
- Error state.

## Docker Tasks

- Add `Dockerfile`.
- Add `docker-compose.yml`.
- Install system dependencies if required by PDF libraries.
- Expose port `8000`.
- Configure `uvicorn` startup command.
- Document Docker usage in README.

## Testing Tasks

### Unit Tests

- Text cleaning
- File extension validation
- Keyword extraction
- Keyword matching
- Section detection
- Score calculation

### Integration Tests

- Analyze endpoint with PDF file
- Analyze endpoint with DOCX file
- Missing file
- Empty job description
- Unsupported file type
- Text extraction failure

### Manual Tests

- Run through the frontend workflow.
- Upload a realistic Turkish CV.
- Paste a Turkish job description.
- Verify that feedback is Turkish.
- Verify that the score looks plausible.

## Postman Tasks

- Create collection named `SmartCV Analyzer`.
- Add environment variable:
  - `base_url = http://localhost:8000`
- Add health check request.
- Add analyze request.
- Add negative test requests.
- Export collection to repository.

## Final GitHub Polish Checklist

- README has clear project description.
- README includes screenshots.
- README includes installation and Docker instructions.
- API spec is complete.
- Scoring logic is transparent.
- Development plan is complete.
- Example response is realistic.
- Repository has clean folder structure.
- `.gitignore` excludes virtual environments, cache files, uploaded files, and model cache if needed.
- License is present.
- No sample personal CV data is committed.
- No paid API keys or secrets are required.
- Project title and description are GitHub-friendly.

## Suggested Future Implementation Order for AI Coding Agent

When moving from documentation to code, ask the coding agent to implement one milestone at a time. Recommended first prompt:

```text
Implement Milestone M1 from DEVELOPMENT_PLAN.md. Create the FastAPI project structure, health endpoint, base router, and minimal dependency files. Do not implement NLP logic yet.
```
