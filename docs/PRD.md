# Product Requirements Document

## Project Overview

SmartCV Analyzer is an AI-powered CV analysis web application. Users upload a CV or resume file and paste a job description manually. The system extracts CV text, analyzes the CV against the job description, calculates a compatibility score, and returns Turkish feedback about strengths, missing keywords, weak sections, and improvement suggestions.

The MVP focuses only on CV/resume analysis. It avoids authentication, databases, paid APIs, and job posting scraping so the project remains realistic, understandable, and suitable for a developer portfolio.

## Problem Statement

Job seekers often struggle to understand whether their CV is aligned with a specific job description. They may miss important keywords, undersell relevant experience, omit standard CV sections, or fail to describe projects in a way that matches employer expectations.

SmartCV Analyzer helps users quickly evaluate how well their CV matches a target job description and provides actionable suggestions in Turkish.

## Goals

- Provide a simple CV-to-job-description analysis workflow.
- Calculate a compatibility score between 0 and 100.
- Identify matched and missing job description keywords.
- Detect missing or weak CV sections.
- Use multilingual semantic similarity to support Turkish and English content.
- Generate user-facing analysis results in Turkish.
- Keep the MVP simple enough for a junior or mid-level portfolio project.
- Produce clean documentation that supports step-by-step implementation by a developer or AI coding agent.

## Target Users

| User Type | Needs |
| --- | --- |
| Junior software developers | Improve CV alignment with job postings |
| Mid-level software developers | Identify missing technical keywords and weak sections |
| Bootcamp graduates | Understand how to strengthen project and skills sections |
| Turkish-speaking job seekers | Receive clear feedback in Turkish |
| Recruiter-adjacent reviewers | Quickly inspect CV-job compatibility in a demo scenario |

## MVP Scope

The MVP includes:

- Single-page web interface
- CV file upload
- Manual job description text area
- PDF and DOCX text extraction
- CV section detection
- Keyword extraction from job description
- Keyword matching against CV text
- Missing keyword detection
- Semantic similarity calculation with sentence-transformers
- Overall compatibility score
- Turkish analysis feedback
- FastAPI endpoint documentation
- Dockerized development setup
- Postman test plan

## Out of Scope

The following features are intentionally excluded from the MVP:

- Authentication and login
- User accounts
- Saved analysis history
- Database
- Payment system
- Paid AI APIs
- Job posting URL scraping
- Browser extension
- Multi-file comparison
- General document analysis
- Advanced resume builder features
- Production-grade monitoring

## User Flow

1. User opens the web application.
2. User clicks Upload CV and selects a PDF or DOCX file.
3. User pastes a job description into a text area.
4. User clicks Analyze.
5. Frontend sends a multipart request to the FastAPI backend.
6. Backend validates file type, file size, and job description content.
7. Backend extracts text from the CV.
8. Backend analyzes sections, keywords, and semantic similarity.
9. Backend calculates the overall score.
10. Backend returns structured JSON with Turkish feedback.
11. Frontend displays the result in a readable format.

## Functional Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-001 | User can upload one CV file | Must |
| FR-002 | System accepts PDF files | Must |
| FR-003 | System accepts DOCX files | Must |
| FR-004 | User can paste a job description manually | Must |
| FR-005 | User can submit the analysis form | Must |
| FR-006 | System extracts readable text from the uploaded CV | Must |
| FR-007 | System detects common CV sections | Must |
| FR-008 | System identifies missing or weak CV sections | Must |
| FR-009 | System extracts important keywords from the job description | Must |
| FR-010 | System identifies keywords present in the CV | Must |
| FR-011 | System identifies important missing keywords | Must |
| FR-012 | System calculates semantic similarity | Must |
| FR-013 | System calculates an overall compatibility score from 0 to 100 | Must |
| FR-014 | System returns suggestions in Turkish | Must |
| FR-015 | Frontend displays score, keywords, section analysis, and suggestions | Must |
| FR-016 | API exposes interactive FastAPI docs | Should |
| FR-017 | Project includes Docker and docker-compose configuration | Should |
| FR-018 | Project includes a Postman testing plan | Should |

## Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Simplicity | The MVP should avoid unnecessary services, queues, databases, and complex frontend frameworks |
| Performance | Typical analysis should complete within 5 to 15 seconds on a development machine after model load |
| Language | UI, docs, API, and code should be English; analysis feedback should be Turkish |
| Privacy | Uploaded files should be processed in memory or temporary storage and not persisted in the MVP |
| Portability | Application should run locally with Docker |
| Maintainability | Code should be modular enough to separate file extraction, NLP, scoring, and API layers |
| Reliability | API should return clear validation errors for missing inputs and unsupported files |
| Cost | The MVP should use open-source local libraries and models only |

## Assumptions

- Target users are mostly Turkish-speaking job seekers and developers.
- CVs and job descriptions may be Turkish, English, or mixed.
- The MVP runs locally or as a small demo deployment.
- The first implementation does not need persistent storage.
- The first implementation can use rule-based keyword and section extraction enhanced by embeddings.
- Turkish feedback can be generated with deterministic templates in the MVP instead of a paid LLM.

## Success Criteria

- A user can analyze a PDF or DOCX CV against a pasted job description in one flow.
- The API returns all required fields:
  - `overall_score`
  - `semantic_similarity`
  - `matched_keywords`
  - `missing_keywords`
  - `section_analysis`
  - `suggestions`
  - `extracted_cv_text_preview`
- The returned suggestions are understandable and useful in Turkish.
- The scoring logic is documented and reproducible.
- The repository looks professional on GitHub.
- Another developer or AI coding agent can implement the project step by step using the documentation.
