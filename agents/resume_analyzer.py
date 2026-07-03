# ============================================================
# Imports
# ============================================================

from google.adk.agents import Agent

from utils.constants import MODEL_NAME


# ============================================================
# Resume Analyzer Agent
# ============================================================

resume_analyzer = Agent(
    name="resume_analyzer",
    model=MODEL_NAME,
    description="Analyzes a candidate resume against a structured Job Description.",
    instruction="""
You are an expert Resume Analyzer.

INPUT

You will receive:

1. The Job Description analysis from another AI agent.

2. The candidate's resume text.

TASK

Compare both carefully.

Return ONLY valid JSON.

{
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "experience_match": "",
    "overall_fit": ""
}

Rules

- Never explain.

- Never use markdown.

- Never use code fences.

- matched_skills must contain only skills found in BOTH JD and resume.

- missing_skills must contain required skills absent from the resume.

- overall_fit should be one sentence.

Return JSON only.
""",
)
