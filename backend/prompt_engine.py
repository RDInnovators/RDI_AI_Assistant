from models import ResearchSubmission, PromptPack


def build_refined_summary(submission: ResearchSubmission) -> dict:
    return {
        "topic": submission.working_title.strip(),
        "field": submission.research_field.strip(),
        "problem_focus": submission.main_problem.strip(),
        "proposed_direction": submission.proposed_solution.strip(),
        "novelty_claim": submission.novelty.strip(),
        "target_output": submission.target_output.strip(),
        "paper_type": submission.paper_type.strip(),
        "preferred_angle": submission.preferred_angle.strip(),
        "constraints": submission.constraints.strip(),
    }


def generate_prompts(submission: ResearchSubmission) -> PromptPack:
    shared_context = f"""
Research topic/title: {submission.working_title}
Field/domain: {submission.research_field}
Main problem: {submission.main_problem}
Why important: {submission.importance}
Proposed solution/method: {submission.proposed_solution}
What is new: {submission.novelty}
Target output: {submission.target_output}
Paper type: {submission.paper_type}
Preferred angle: {submission.preferred_angle}
Known keywords: {submission.known_keywords}
Similar papers/methods known: {submission.similar_papers or "Not provided"}
Data available: {submission.data_available}
Data source details: {submission.data_source_details or "Not provided"}
Tools available: {submission.tools_available or "Not provided"}
Constraints: {submission.constraints}
Target venue: {submission.target_venue or "Not provided"}
Deadline: {submission.deadline or "Not provided"}
What AI help is needed first: {submission.ai_help_needed_first}
""".strip()

    bohrium_prompt = f"""
Act as an academic literature discovery assistant.

Using the following research context, find the most relevant academic papers and research directions.

{shared_context}

Return:
1. recent core papers
2. survey/review papers
3. benchmark/comparative papers
4. common datasets
5. common evaluation metrics
6. repeated limitations in the literature
7. likely research gaps
8. papers most similar to this idea

Format the output clearly with:
- Title
- Year
- Main contribution
- Method
- Dataset/context
- Metrics
- Limitation
- Relevance to this idea
""".strip()

    perplexity_prompt = f"""
Act as a fast research scout with sourced answers.

Using the context below, give a quick but high-value overview of the research landscape.

{shared_context}

I need:
1. recent important papers
2. major methods being used
3. top keywords/subtopics to search
4. likely datasets and benchmarks
5. likely journals/conferences that publish similar work
6. a quick assessment of whether this idea looks broad, common, niche, or promising

Please keep the response structured and source-oriented.
""".strip()

    gemini_prompt = f"""
Act as a strict academic critic.

Review this research idea and challenge it.

{shared_context}

Please analyze:
1. whether the novelty is really strong or weak
2. hidden assumptions
3. likely reviewer objections
4. what is missing from the idea
5. whether the framing can be improved
6. what alternative angle may make it more publishable
7. whether this is better suited for conference, journal, review, or thesis work

Be critical, specific, and practical.
""".strip()

    chatgpt_prompt = f"""
Act as my academic research strategist and writing planner.

Based on the following research context:

{shared_context}

Generate:
1. a refined research title
2. a strong problem statement
3. a clear novelty statement
4. research objectives
5. research questions
6. a keyword bank for literature search
7. 2-3 possible methodology directions
8. the best next step for turning this into a publishable paper

Keep the output structured, formal, and publication-oriented.
""".strip()

    return PromptPack(
        bohrium=bohrium_prompt,
        perplexity=perplexity_prompt,
        gemini=gemini_prompt,
        chatgpt=chatgpt_prompt,
    )