const API_BASE = "http://127.0.0.1:8000";

const form = document.getElementById("researchForm");
const resultSection = document.getElementById("resultSection");
const resultContent = document.getElementById("resultContent");
const submitBtn = document.getElementById("submitBtn");

function getFormData() {
  return {
    working_title: document.getElementById("working_title").value.trim(),
    research_field: document.getElementById("research_field").value.trim(),
    main_problem: document.getElementById("main_problem").value.trim(),
    importance: document.getElementById("importance").value.trim(),
    proposed_solution: document.getElementById("proposed_solution").value.trim(),
    novelty: document.getElementById("novelty").value.trim(),
    target_output: document.getElementById("target_output").value,
    paper_type: document.getElementById("paper_type").value,
    preferred_angle: document.getElementById("preferred_angle").value.trim(),
    known_keywords: document.getElementById("known_keywords").value.trim(),
    similar_papers: document.getElementById("similar_papers").value.trim(),
    data_available: document.getElementById("data_available").value,
    data_source_details: document.getElementById("data_source_details").value.trim(),
    tools_available: document.getElementById("tools_available").value.trim(),
    constraints: document.getElementById("constraints").value.trim(),
    deadline: document.getElementById("deadline").value.trim(),
    target_venue: document.getElementById("target_venue").value.trim(),
    ai_help_needed_first: document.getElementById("ai_help_needed_first").value.trim(),
  };
}

function copyText(text) {
  navigator.clipboard.writeText(text)
    .then(() => alert("Copied to clipboard"))
    .catch(() => alert("Copy failed"));
}

function buildPromptBox(title, promptText) {
  return `
    <div class="result-box">
      <h3>${title}</h3>
      <pre>${escapeHtml(promptText)}</pre>
      <button class="copy-btn" onclick='copyPrompt(${JSON.stringify(promptText)})'>Copy Prompt</button>
    </div>
  `;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

window.copyPrompt = function(promptText) {
  copyText(promptText);
};

function renderResult(data) {
  const summary = data.refined_summary;
  const prompts = data.prompts;
  const scores = data.scores;

  resultContent.innerHTML = `
    <div class="result-box">
      <h3>Recommended AI: ${data.recommended_ai}</h3>
      <p><strong>Reason:</strong> ${data.recommendation_reason}</p>
      <p><strong>Next step:</strong> ${data.next_step}</p>
    </div>

    <div class="result-box">
      <h3>Refined Summary</h3>
      <p><strong>Topic:</strong> ${escapeHtml(summary.topic)}</p>
      <p><strong>Field:</strong> ${escapeHtml(summary.field)}</p>
      <p><strong>Problem Focus:</strong> ${escapeHtml(summary.problem_focus)}</p>
      <p><strong>Proposed Direction:</strong> ${escapeHtml(summary.proposed_direction)}</p>
      <p><strong>Novelty Claim:</strong> ${escapeHtml(summary.novelty_claim)}</p>
      <p><strong>Target Output:</strong> ${escapeHtml(summary.target_output)}</p>
      <p><strong>Paper Type:</strong> ${escapeHtml(summary.paper_type)}</p>
      <p><strong>Preferred Angle:</strong> ${escapeHtml(summary.preferred_angle)}</p>
      <p><strong>Constraints:</strong> ${escapeHtml(summary.constraints)}</p>
    </div>

    <div class="result-box">
      <h3>AI Scores</h3>
      <div class="score-grid">
        <div class="score-item"><strong>ChatGPT:</strong> ${scores.ChatGPT}</div>
        <div class="score-item"><strong>Bohrium:</strong> ${scores.Bohrium}</div>
        <div class="score-item"><strong>Perplexity:</strong> ${scores.Perplexity}</div>
        <div class="score-item"><strong>Gemini:</strong> ${scores.Gemini}</div>
      </div>
    </div>

    ${buildPromptBox("Bohrium Prompt", prompts.bohrium)}
    ${buildPromptBox("Perplexity Prompt", prompts.perplexity)}
    ${buildPromptBox("Gemini Prompt", prompts.gemini)}
    ${buildPromptBox("ChatGPT Prompt", prompts.chatgpt)}
  `;

  resultSection.classList.remove("hidden");
  resultSection.scrollIntoView({ behavior: "smooth" });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.textContent = "Generating...";

  try {
    const payload = getFormData();

    const response = await fetch(`${API_BASE}/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Failed to submit form");
    }

    const data = await response.json();
    renderResult(data);
  } catch (error) {
    console.error(error);
    alert("Something went wrong. Check backend and try again.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Generate Prompt Pack";
  }
});