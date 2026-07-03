"""
File:
    resume_analyzer.py

Purpose:
    Defines the Resume Analyzer Agent.

Responsibilities:
    - Compare a Resume against the structured JD analysis.
    - Identify strengths, weaknesses and missing skills.
    - Produce structured JSON output.

Dependencies:
    - Google ADK
    - prompts package
    - utils.constants
"""

# ==========================================================
# Imports
# ==========================================================

from google.adk.agents import LlmAgent

from prompts import get_resume_prompt

from utils.constants import (
    MODEL_NAME,
    RESUME_ANALYSIS_KEY,
)

# ==========================================================
# Resume Analyzer
# ==========================================================

resume_analyzer = LlmAgent(
    name="resume_analyzer",
    model=MODEL_NAME,
    description=(
        "Evaluates how well a candidate's resume matches the supplied "
        "Job Description analysis."
    ),
    instruction=get_resume_prompt(),
    output_key=RESUME_ANALYSIS_KEY,
)
