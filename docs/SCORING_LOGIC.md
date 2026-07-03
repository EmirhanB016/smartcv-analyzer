# Scoring Logic

## CV-Job Description Matching Strategy

The MVP combines three analysis dimensions:

1. Semantic similarity between the full CV text and job description
2. Keyword match ratio between important job description keywords and CV content
3. CV section completeness and quality

This hybrid approach is more useful than keyword matching alone. A CV may use slightly different wording than a job description but still be semantically relevant. At the same time, explicit keywords still matter because many hiring workflows and applicant tracking systems rely on visible terms.

## Keyword Extraction Logic

The keyword extraction service should extract important terms from the job description.

Recommended MVP process:

1. Convert text to a normalized form for analysis.
2. Preserve original display form where possible.
3. Remove common Turkish and English stop words.
4. Extract unigrams, bigrams, and selected trigrams.
5. Prefer technical terms, tools, frameworks, responsibilities, and methodologies.
6. Deduplicate keywords case-insensitively.
7. Limit the final keyword list to the top 20 to 30 terms.

Example job description:

```text
We are looking for a Python developer with FastAPI, Docker, SQL, REST API,
Git, CI/CD, and cloud deployment experience.
```

Example extracted keywords:

```json
[
  "Python",
  "FastAPI",
  "Docker",
  "SQL",
  "REST API",
  "Git",
  "CI/CD",
  "cloud deployment"
]
```

## Keyword Matching Logic

Keyword matching checks whether extracted job description keywords appear in the CV.

Recommended matching rules:

- Use case-insensitive matching.
- Normalize Turkish characters consistently without destroying original display text.
- Match exact keywords first.
- Support simple phrase matching for terms like `REST API` and `machine learning`.
- Consider common variants when practical.

Example variants:

| Keyword | Possible Variants |
| --- | --- |
| `JavaScript` | `JS`, `Javascript` |
| `PostgreSQL` | `Postgres` |
| `CI/CD` | `CI CD`, `continuous integration` |
| `REST API` | `RESTful API`, `REST APIs` |

The first version can use a small manually maintained synonym map for common software development terms.

## Missing Keyword Detection

Missing keywords are important job description keywords that are not detected in the CV.

```text
missing_keywords = extracted_job_keywords - matched_keywords
```

Missing keywords should not automatically mean the CV is bad. The feedback should be careful:

- If the user has that experience, suggest making it more visible.
- If the user does not have that experience, suggest not adding false claims.

Example Turkish suggestion:

```text
CI/CD deneyiminiz varsa bu bilgiyi projeler veya iş deneyimi bölümünde daha görünür hale getirebilirsiniz.
```

## Section Analysis Logic

The MVP should detect these sections:

- Contact information
- Professional summary or profile
- Skills
- Work experience
- Education
- Projects
- Certifications

Each section receives one status:

| Status | Meaning |
| --- | --- |
| `present` | Section is detected and appears useful |
| `weak` | Section exists but seems too short or lacks relevant detail |
| `missing` | Section is not detected |

### Section Detection Rules

Use heading-based detection for Turkish and English headings.

Example:

| Section | Headings |
| --- | --- |
| Contact information | Contact, Contact Information, İletişim |
| Summary | Summary, Profile, Professional Summary, Özet, Profil |
| Skills | Skills, Technical Skills, Yetenekler, Teknik Yetenekler |
| Work experience | Experience, Work Experience, İş Deneyimi, Deneyim |
| Education | Education, Eğitim |
| Projects | Projects, Projeler |
| Certifications | Certifications, Certificates, Sertifikalar |

### Weak Section Rules

A section may be marked `weak` when:

- It is very short.
- It contains only generic wording.
- It lacks technical keywords relevant to the job description.
- The projects section lacks technologies or outcomes.
- The work experience section lacks responsibilities, impact, or tools.

## Semantic Similarity Calculation

Semantic similarity compares the meaning of the CV and job description.

Recommended model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Recommended steps:

1. Clean CV text.
2. Clean job description text.
3. Generate embedding for CV text.
4. Generate embedding for job description text.
5. Calculate cosine similarity.
6. Clamp the result between 0 and 1.

Example:

```text
semantic_similarity = cosine_similarity(cv_embedding, job_description_embedding)
```

## Overall Score Formula

Recommended MVP weights:

| Component | Weight |
| --- | ---: |
| Semantic similarity | 50% |
| Keyword match ratio | 30% |
| Section completeness | 20% |

Formula:

```text
overall_score =
  (semantic_similarity * 50)
  + (keyword_match_ratio * 30)
  + (section_score * 20)
```

Where:

```text
keyword_match_ratio = matched_keywords_count / total_extracted_keywords_count
```

Section status values:

| Status | Score |
| --- | ---: |
| `present` | 1.0 |
| `weak` | 0.5 |
| `missing` | 0.0 |

```text
section_score = average(section_status_scores)
```

Final result:

```text
overall_score = round(clamp(overall_score, 0, 100))
```

## Example Scoring Breakdown

Example inputs:

| Metric | Value |
| --- | ---: |
| Semantic similarity | 0.82 |
| Extracted keywords | 10 |
| Matched keywords | 7 |
| Keyword match ratio | 0.70 |
| Section score | 0.75 |

Calculation:

```text
semantic component = 0.82 * 50 = 41
keyword component = 0.70 * 30 = 21
section component = 0.75 * 20 = 15

overall_score = 41 + 21 + 15 = 77
```

Final score:

```text
77 / 100
```

Example Turkish summary:

```text
CV'niz iş ilanıyla %77 oranında uyumlu görünüyor. Genel teknik altyapınız ilandaki beklentilerle örtüşüyor, ancak bazı anahtar kelimeler ve bölüm detayları daha görünür hale getirilebilir.
```

## Score Interpretation

| Score Range | Meaning | Turkish Feedback Direction |
| --- | --- | --- |
| 0-39 | Low match | Major improvements needed |
| 40-59 | Moderate match | Some relevant content exists, but gaps are significant |
| 60-79 | Good match | CV is mostly aligned, targeted improvements recommended |
| 80-100 | Strong match | CV is highly aligned, minor polishing recommended |

## Feedback Generation Rules

The MVP should use deterministic Turkish templates.

Feedback should:

- Be practical and specific.
- Avoid telling users to add skills they do not have.
- Mention missing keywords conditionally.
- Prioritize the most important gaps.
- Keep language clear and encouraging.

Example templates:

```text
CV'niz iş ilanıyla genel olarak iyi düzeyde uyumlu görünüyor.
```

```text
{keyword_list} deneyiminiz varsa bu anahtar kelimeleri CV'nizde daha görünür şekilde konumlandırmanız önerilir.
```

```text
{section_name} bölümü eksik görünüyor. Bu bölümü eklemek CV'nizin daha bütünlüklü görünmesine yardımcı olabilir.
```
