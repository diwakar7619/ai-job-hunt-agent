"""
File:
    quality_checker.py

Purpose:
    Defines the Quality Checker Agent.
"""

from google.adk.agents import LlmAgent
from prompts import get_quality_prompt
from utils.constants import MODEL_NAME, QUALITY_CHECK_KEY

quality_checker = LlmAgent(
    name="quality_checker",
    model=MODEL_NAME,
    description=(
        "Independent Quality Assurance Agent responsible for validating the "
        "consistency, completeness, ATS relevance, and actionability of previous "
        "pipeline outputs before recruiter outreach generation."
    ),
    instruction=get_quality_prompt(),
    output_key=QUALITY_CHECK_KEY,
)
