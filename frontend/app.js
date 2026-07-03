const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024;
const SUPPORTED_EXTENSIONS = [".pdf", ".docx"];

const form = document.querySelector("#analysis-form");
const fileInput = document.querySelector("#cv-file");
const jobDescriptionInput = document.querySelector("#job-description");
const analyzeButton = document.querySelector("#analyze-button");
const buttonLabel = document.querySelector("#button-label");
const clientError = document.querySelector("#client-error");

const states = {
  empty: document.querySelector("#empty-state"),
  loading: document.querySelector("#loading-state"),
  error: document.querySelector("#error-state"),
  results: document.querySelector("#results-state"),
};

const output = {
  errorTitle: document.querySelector("#error-title"),
  errorMessage: document.querySelector("#error-message"),
  errorCode: document.querySelector("#error-code"),
  overallScore: document.querySelector("#overall-score"),
  semanticSimilarity: document.querySelector("#semantic-similarity"),
  matchedKeywords: document.querySelector("#matched-keywords"),
  matchedEmpty: document.querySelector("#matched-empty"),
  matchedCount: document.querySelector("#matched-count"),
  missingKeywords: document.querySelector("#missing-keywords"),
  missingEmpty: document.querySelector("#missing-empty"),
  missingCount: document.querySelector("#missing-count"),
  sectionAnalysis: document.querySelector("#section-analysis"),
  suggestionsList: document.querySelector("#suggestions-list"),
  textPreview: document.querySelector("#text-preview"),
};

const errorMessages = {
  MISSING_FILE: "Please upload a PDF or DOCX CV.",
  EMPTY_JOB_DESCRIPTION: "Please paste a job description before analyzing.",
  UNSUPPORTED_FILE_TYPE: "Only PDF and DOCX files are supported.",
  FILE_TOO_LARGE: "The selected file is larger than the 5 MB limit.",
  TEXT_EXTRACTION_FAILED: "Readable text could not be extracted from this CV.",
  ANALYSIS_FAILED: "The analysis could not be completed. Please try again.",
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearClientError();

  const validationMessage = validateForm();
  if (validationMessage) {
    showClientError(validationMessage);
    return;
  }

  setLoading(true);
  showState("loading");

  try {
    const result = await submitAnalysis();
    renderResults(result);
    showState("results");
  } catch (error) {
    renderError(error);
    showState("error");
  } finally {
    setLoading(false);
  }
});

fileInput.addEventListener("change", clearClientError);
jobDescriptionInput.addEventListener("input", clearClientError);

function validateForm() {
  const file = fileInput.files[0];
  const jobDescription = jobDescriptionInput.value.trim();

  if (!file) {
    return "Please upload your CV.";
  }

  const extension = getFileExtension(file.name);
  if (!SUPPORTED_EXTENSIONS.includes(extension)) {
    return "Please choose a PDF or DOCX file.";
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "Please choose a file smaller than 5 MB.";
  }

  if (!jobDescription) {
    return "Please paste the job description.";
  }

  return "";
}

async function submitAnalysis() {
  const formData = new FormData();
  formData.append("cv_file", fileInput.files[0]);
  formData.append("job_description", jobDescriptionInput.value.trim());

  const response = await fetch("/api/v1/analyze", {
    method: "POST",
    body: formData,
  });

  const payload = await parseJsonResponse(response);
  if (!response.ok) {
    throw buildApiError(response, payload);
  }

  return payload;
}

async function parseJsonResponse(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}

function buildApiError(response, payload) {
  const detail = payload.detail || {};
  const code = detail.code || "REQUEST_FAILED";
  const message =
    errorMessages[code] ||
    detail.message ||
    `Request failed with status ${response.status}.`;

  return {
    code,
    message,
    status: response.status,
  };
}

function renderResults(result) {
  const score = Number.isFinite(result.overall_score) ? result.overall_score : 0;
  const similarity = Number.isFinite(result.semantic_similarity)
    ? result.semantic_similarity
    : 0;

  output.overallScore.textContent = `${score} / 100`;
  output.semanticSimilarity.textContent = formatPercent(similarity);

  renderKeywordList({
    container: output.matchedKeywords,
    emptyElement: output.matchedEmpty,
    countElement: output.matchedCount,
    keywords: result.matched_keywords || [],
    chipClass: "matched",
  });

  renderKeywordList({
    container: output.missingKeywords,
    emptyElement: output.missingEmpty,
    countElement: output.missingCount,
    keywords: result.missing_keywords || [],
    chipClass: "missing",
  });

  renderSections(result.section_analysis || []);
  renderSuggestions(result.suggestions || []);
  output.textPreview.textContent =
    result.extracted_cv_text_preview || "No extracted text preview returned.";
  output.textPreview.scrollTop = 0;
}

function renderKeywordList({
  container,
  emptyElement,
  countElement,
  keywords,
  chipClass,
}) {
  clearElement(container);
  countElement.textContent = String(keywords.length);
  emptyElement.hidden = keywords.length > 0;

  keywords.forEach((keyword) => {
    const chip = document.createElement("span");
    chip.className = `chip ${chipClass}`;
    chip.textContent = keyword;
    container.appendChild(chip);
  });
}

function renderSections(sections) {
  clearElement(output.sectionAnalysis);

  sections.forEach((section) => {
    const item = document.createElement("article");
    item.className = "section-item";

    const header = document.createElement("div");
    header.className = "section-item-header";

    const name = document.createElement("span");
    name.className = "section-name";
    name.textContent = section.section || "Section";

    const status = document.createElement("span");
    const normalizedStatus = normalizeStatus(section.status);
    status.className = `status-label status-${normalizedStatus}`;
    status.textContent = normalizedStatus;

    const message = document.createElement("p");
    message.className = "section-message";
    message.textContent = section.message || "";

    header.append(name, status);
    item.append(header, message);
    output.sectionAnalysis.appendChild(item);
  });
}

function renderSuggestions(suggestions) {
  clearElement(output.suggestionsList);

  if (suggestions.length === 0) {
    const item = document.createElement("li");
    item.textContent = "No suggestions returned.";
    output.suggestionsList.appendChild(item);
    return;
  }

  suggestions.forEach((suggestion) => {
    const item = document.createElement("li");
    item.textContent = suggestion;
    output.suggestionsList.appendChild(item);
  });
}

function renderError(error) {
  output.errorTitle.textContent = "Unable to analyze CV";
  output.errorMessage.textContent = error.message || "Something went wrong.";
  output.errorCode.textContent = error.code ? `Error code: ${error.code}` : "";
}

function showState(activeState) {
  Object.entries(states).forEach(([name, element]) => {
    element.hidden = name !== activeState;
  });
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  buttonLabel.textContent = isLoading ? "Analyzing..." : "Analyze CV";
}

function showClientError(message) {
  clientError.textContent = message;
  clientError.hidden = false;
}

function clearClientError() {
  clientError.textContent = "";
  clientError.hidden = true;
}

function clearElement(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}

function normalizeStatus(status) {
  if (status === "present" || status === "weak" || status === "missing") {
    return status;
  }

  return "missing";
}

function formatPercent(value) {
  const percent = Math.max(0, Math.min(1, value)) * 100;
  return `${percent.toFixed(2)}%`;
}

function getFileExtension(filename) {
  const dotIndex = filename.lastIndexOf(".");
  if (dotIndex === -1) {
    return "";
  }

  return filename.slice(dotIndex).toLowerCase();
}
