from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ResearchSubmission(BaseModel):
    working_title: str = Field(..., min_length=3)
    research_field: str = Field(..., min_length=2)
    main_problem: str = Field(..., min_length=5)
    importance: str = Field(..., min_length=5)
    proposed_solution: str = Field(..., min_length=5)
    novelty: str = Field(..., min_length=3)
    target_output: str = Field(..., min_length=2)
    paper_type: str = Field(..., min_length=2)
    preferred_angle: str = Field(..., min_length=2)
    known_keywords: str = Field(..., min_length=2)
    constraints: str = Field(..., min_length=2)
    ai_help_needed_first: str = Field(..., min_length=2)

    similar_papers: Optional[str] = ""
    data_available: Optional[str] = "No"
    data_source_details: Optional[str] = ""
    tools_available: Optional[str] = ""
    deadline: Optional[str] = ""
    target_venue: Optional[str] = ""


class PromptPack(BaseModel):
    bohrium: str
    perplexity: str
    gemini: str
    chatgpt: str


class SubmissionResponse(BaseModel):
    refined_summary: Dict[str, str]
    recommended_ai: str
    recommendation_reason: str
    next_step: str
    prompts: PromptPack
    scores: Dict[str, int]