"""
File:
    jd_analyzer.py

Purpose:
    Defines the Job Description Analyzer Agent.

Responsibilities:
    - Extract structured information from a Job Description.
    - Produce deterministic JSON output.
    - Store the parsed result in the shared session state.

Dependencies:
    - Google ADK
    - prompts package
    - utils.constants
"""

# ==========================================================
# Imports
# ==========================================================

from google.adk.agents import LlmAgent

from prompts import get_jd_prompt

from utils.constants import (
    MODEL_NAME,
    JD_ANALYSIS_KEY,
)

# ==========================================================
# Job Description Analyzer
# ==========================================================

jd_analyzer = LlmAgent(
    name="jd_analyzer",
    model=MODEL_NAME,
    description=(
        "Extracts structured information from a Job Description including "
        "required skills, preferred skills, responsibilities, experience "
        "requirements, and a concise summary."
    ),
    instruction=get_jd_prompt(),
    output_key=JD_ANALYSIS_KEY,
)
