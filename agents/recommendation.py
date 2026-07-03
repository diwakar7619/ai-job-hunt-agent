"""
File:
    recommendation.py

Purpose:
    Defines the Recommendation Agent.

Responsibilities:
    - Analyze the Resume Analysis and Job Description Analysis.
    - Recommend skills to learn.
    - Suggest projects.
    - Suggest resume improvements.
    - Prepare interview focus areas.

Dependencies:
    - Google ADK
    - prompts package
    - utils.constants
"""

# ==========================================================
# Imports
# ==========================================================

from google.adk.agents import LlmAgent

from prompts import get_recommendation_prompt

from utils.constants import (
    MODEL_NAME,
    RECOMMENDATION_KEY,
)

# ==========================================================
# Recommendation Agent
# ==========================================================

recommendation_agent = LlmAgent(
    name="recommendation_agent",
    model=MODEL_NAME,
    description=(
        "Provides personalized career recommendations by comparing "
        "the candidate's resume against the analyzed Job Description."
    ),
    instruction=get_recommendation_prompt(),
    output_key=RECOMMENDATION_KEY,
)
