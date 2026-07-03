"""
File:
    outreach_writer.py

Purpose:
    Defines the Outreach Writer Agent.

Responsibilities:
    - Generate a personalized ATS-friendly cover letter.
    - Generate a professional application email.
    - Produce structured JSON.

Dependencies:
    - Google ADK
    - prompts package
    - utils.constants
"""

# ==========================================================
# Imports
# ==========================================================

from google.adk.agents import LlmAgent

from prompts import get_outreach_prompt

from utils.constants import (
    MODEL_NAME,
    OUTREACH_KEY,
)

# ==========================================================
# Outreach Writer
# ==========================================================

outreach_writer = LlmAgent(
    name="outreach_writer",
    model=MODEL_NAME,
    description=(
        "Generates a personalized cover letter and professional "
        "application email based on the candidate profile and "
        "job description."
    ),
    instruction=get_outreach_prompt(),
    output_key=OUTREACH_KEY,
)
