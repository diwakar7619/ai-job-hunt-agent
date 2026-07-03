# ============================================================
# Imports
# ============================================================

from google.adk.agents import LlmAgent

from utils.constants import (
    MODEL_NAME,
    RECOMMENDATION_KEY,
)


# ============================================================
# Recommendation Agent
# ============================================================

recommendation_agent = LlmAgent(
    name="recommendation_agent",
    model=MODEL_NAME,
    description="Provides personalized recommendations based on resume analysis.",
    output_key=RECOMMENDATION_KEY,
    instruction="""
You are an expert AI Career Coach.

INPUT

You will receive:

1. Job Description Analysis

2. Resume Analysis

TASK

Generate ONLY valid JSON.

{
    "priority_skills": [],
    "learning_plan": [],
    "resume_improvements": [],
    "project_recommendations": [],
    "interview_focus": []
}

Rules

- Never explain.

- Never use markdown.

- Never use code fences.

- Prioritize the missing skills.

- Recommend practical projects.

- Keep every recommendation concise.

Return JSON only.
""",
)
