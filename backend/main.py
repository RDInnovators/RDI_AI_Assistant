from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import ResearchSubmission, SubmissionResponse
from recommender import recommend_ai
from prompt_engine import generate_prompts, build_refined_summary
from sheets import save_submission_to_sheet

app = FastAPI(title="RDI AI Prompt Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RDI AI Prompt Assistant backend is running."}


@app.post("/submit", response_model=SubmissionResponse)
def submit_research(submission: ResearchSubmission):
    recommendation = recommend_ai(submission)
    prompts = generate_prompts(submission)
    refined_summary = build_refined_summary(submission)

    save_submission_to_sheet(submission)

    return SubmissionResponse(
        refined_summary=refined_summary,
        recommended_ai=recommendation["recommended_ai"],
        recommendation_reason=recommendation["recommendation_reason"],
        next_step=recommendation["next_step"],
        prompts=prompts,
        scores=recommendation["scores"],
    )