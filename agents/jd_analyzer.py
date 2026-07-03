# ============================================================
# Imports
# ============================================================

from google.adk.agents import LlmAgent

from utils.constants import (
    MODEL_NAME,
    JD_ANALYSIS_KEY,
)

# ============================================================
# JD Analyzer
# ============================================================

jd_analyzer = LlmAgent(
    name="jd_analyzer",
    model=MODEL_NAME,
    description="Analyzes a Job Description.",
    output_key=JD_ANALYSIS_KEY,
    instruction="""
You are an expert Job Description Analyzer.

Analyze the user's Job Description.

Return ONLY valid JSON.

{
    "job_title":"",
    "required_skills":[],
    "preferred_skills":[],
    "experience_required":"",
    "responsibilities":[],
    "summary":""
}

Return JSON only.
""",
)
