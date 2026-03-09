from typing import Dict
from models import ResearchSubmission


AI_OPTIONS = ["ChatGPT", "Bohrium", "Perplexity", "Gemini"]


def _contains_any(text: str, keywords: list[str]) -> bool:
    text_lower = (text or "").lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def recommend_ai(submission: ResearchSubmission) -> Dict[str, object]:
    scores = {ai: 0 for ai in AI_OPTIONS}

    combined_text = " ".join([
        submission.working_title,
        submission.main_problem,
        submission.proposed_solution,
        submission.novelty,
        submission.ai_help_needed_first,
        submission.paper_type,
        submission.target_output,
        submission.preferred_angle,
    ]).lower()

    # ChatGPT scoring
    if _contains_any(combined_text, [
        "refine", "structure", "writing", "draft", "outline",
        "methodology", "problem statement", "novelty", "abstract"
    ]):
        scores["ChatGPT"] += 4

    if _contains_any(submission.ai_help_needed_first, [
        "writing", "title", "problem statement", "methodology", "outline"
    ]):
        scores["ChatGPT"] += 5

    # Bohrium scoring
    if _contains_any(combined_text, [
        "journal", "review", "experimental", "literature",
        "academic", "benchmark", "dataset", "metrics", "survey"
    ]):
        scores["Bohrium"] += 5

    if not submission.similar_papers.strip():
        scores["Bohrium"] += 3

    if _contains_any(submission.ai_help_needed_first, [
        "literature", "papers", "review papers", "datasets", "metrics", "research gap"
    ]):
        scores["Bohrium"] += 5

    # Perplexity scoring
    if _contains_any(combined_text, [
        "overview", "broad", "explore", "fast search", "quick",
        "current", "recent", "discover"
    ]):
        scores["Perplexity"] += 4

    if _contains_any(submission.ai_help_needed_first, [
        "fast search", "quick overview", "recent papers", "broad discovery"
    ]):
        scores["Perplexity"] += 5

    # Gemini scoring
    if _contains_any(combined_text, [
        "second opinion", "critique", "alternative", "validate",
        "challenge", "different view"
    ]):
        scores["Gemini"] += 4

    if _contains_any(submission.ai_help_needed_first, [
        "second opinion", "critique", "validate novelty", "alternative framing"
    ]):
        scores["Gemini"] += 5

    # Additional logic by paper type / maturity
    if submission.paper_type.lower() in ["review", "survey"]:
        scores["Bohrium"] += 4
        scores["ChatGPT"] += 2

    if submission.target_output.lower() in ["journal paper", "journal", "thesis"]:
        scores["Bohrium"] += 3
        scores["ChatGPT"] += 2

    if len(submission.working_title.split()) < 4:
        scores["ChatGPT"] += 2

    # Pick winner
    recommended_ai = max(scores, key=scores.get)

    reasons = {
        "ChatGPT": "Best first step for structuring the idea, refining novelty, and preparing writing-ready research direction.",
        "Bohrium": "Best first step for academic-heavy literature discovery, benchmark papers, datasets, evaluation metrics, and research-gap exploration.",
        "Perplexity": "Best first step for fast sourced discovery and quick broad exploration of the topic landscape.",
        "Gemini": "Best first step for second-opinion critique, alternative framing, and novelty validation."
    }

    next_steps = {
        "ChatGPT": "Refine the topic, problem statement, novelty, and methodology direction before doing external paper search.",
        "Bohrium": "Search for survey papers, recent studies, benchmark works, common datasets, and standard evaluation metrics.",
        "Perplexity": "Run a fast broad paper search to identify important authors, recent work, and major subtopics.",
        "Gemini": "Ask for critique of the idea, missing logic, and alternate high-potential framing before moving ahead."
    }

    return {
        "recommended_ai": recommended_ai,
        "recommendation_reason": reasons[recommended_ai],
        "next_step": next_steps[recommended_ai],
        "scores": scores,
    }